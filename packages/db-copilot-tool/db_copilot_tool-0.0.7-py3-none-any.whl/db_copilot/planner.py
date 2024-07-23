import json
from typing import Any, Dict, Iterator, List, OrderedDict, Union
import re
from datetime import datetime

from pandas import DataFrame
from db_copilot.contract.plan_core import Planner
from db_copilot.contract.tool_core import Cell, CodeBlock, CodeExecuteResult, PythonExecuteResult, SQLExecuteResult, Tool, CodeInfo
from db_copilot.contract.db_provider import DBProviderAgent
from db_copilot.contract.llm_core import LLM, PromptComposer
from db_copilot.contract.memory_core import MessageRole, MemoryManager, Message
from db_copilot.contract.utils import text_utils

from db_copilot.tool import SQLExecuteTool, PythonExecuteTool
from db_copilot.llm import StaticPromptComposer, DynamicPromptComposer, CompoundPromptComposer
from db_copilot.telemetry import track_activity, get_logger

logger = get_logger("db_copilot.planner")

class DefaultPlanner(Planner):

    DEFAULT_SYSTEM_INTERRUPT_MESSAGE_TEMPLATE = """
Since you generate a piece of code, this triggers a system interrupt to execute the code.
The code execution result is:

{result_text}

If the above cells is incomplete to form a response, please give me the cells after them.
Make sure that the newly generated cells will not overwhelm the existing information of the above cells.
If the above cells is complete to form a response, please just return "<Cell>The End</Cell>" as an end signal.

Here are some instructions that can guide you how to generate the next message:
- If the execution result is an exception message (i.e., <ErrorMessage>...</ErrorMessage>), please generate a new code block cell in which the exception could be addressed.
- If the execution result is a diagram (or diagram json data), the results have been visualized to the users. You should never provide some other code blocks that show the diagrams again: that makes users feeling verbose.
- You should never provide cells like "the following pie chart shows xxxx:". Insteadly, for such cases, you should provide "the above pie chart shows xxxx.".
- You response should never contain any reply words like "Great!", "Certainly!", "Sorry", etc.
"""

    def __init__(self,
            tool_dict: OrderedDict[str, Tool],
            llm: LLM,
            max_iterations: int = 10,
            stream: bool = True,
            system_interrupt_message_template: str = DEFAULT_SYSTEM_INTERRUPT_MESSAGE_TEMPLATE
        ) -> None:
        self.tool_dict = tool_dict
        self.llm = llm
        self.max_iterations = max_iterations
        self.stream = stream
        self.system_interrupt_message_template = system_interrupt_message_template

    @classmethod
    def from_db_provider_agent(cls, db_provider_agent: DBProviderAgent, llm: LLM, **kwargs):
        return cls({
                str(db_provider_agent.sql_dialect): SQLExecuteTool(db_provider_agent),
                'python': PythonExecuteTool()
            },
            llm=llm,
        )

    def generate(self,
            prompt: Union[str, PromptComposer],
            memory_manager: MemoryManager,
            messages: List[Message] = None,
            temperature: float = None,
            top_p: float = None,                 
            **kwargs
        ) -> Iterator[List[Cell]]:
        with track_activity(logger, "planner") as activity_logger:
            activity_logger.activity_info["temperature"] = temperature
            activity_logger.activity_info["top_p"] = top_p

            cells: List[Cell] = []
            stop = self.stop_symbols
            cur_prompt_composer = prompt
            if isinstance(prompt, str):
                cur_prompt_composer = StaticPromptComposer(prompt)
            if not messages:
                raise ValueError('messages cannot be None or empty')

            legacy_memory : List[Any] = [] # Keep back compatibility
            messages_0 = messages.copy()

            # generate at most self.max_iterations <Cell>...</Cell> blocks
            for iter_id in range(self.max_iterations):
                activity_logger.info(f"start generating cells, iteration {iter_id}")
                # pieces: the content stream of the current cell     
                pieces = self.llm.chat(
                    messages=[m.to_dict() for m in messages],
                    prompt=cur_prompt_composer,
                    stop=stop,
                    stream=self.stream,
                    temperature=temperature,
                    top_p=top_p,                
                    **kwargs
                )

                stop_flag = False
                n_previous_cells = len(cells)
                for i, piece in enumerate(pieces):
                    if i == 0:
                        init_content = piece
                        if self.response_symbol_start in init_content:
                            init_content = text_utils.lstrip_text(init_content, self.response_symbol_start)
                        cells.append(Cell(content=init_content, code_info=None))
                    else:
                        cells[-1].content += piece
                    
                    if len(cells[-1].content.strip()) > 0 and not cells[-1].content.strip().startswith(self.cell_symbol_start):
                        cells[-1].content = f'{self.cell_symbol_start}\n' + cells[-1].content

                    if self.should_stop(cells):
                        cells = cells[:-1]
                        stop_flag = True
                        break

                    cell_contents = cells[-1].content.split(self.cell_symbol_start)[1:]
                    cells = cells[:-1]
                    cells += [
                        Cell(content=f'{self.cell_symbol_start}{content}', code_info=None)
                        for content in cell_contents
                        if not content.strip().lower().startswith("the end")
                    ]

                    yield cells
                if stop_flag:
                    activity_logger.info(f"finish generating cells, iteration {iter_id}, generated {len(cells)} cells")
                    yield cells
                    break
                
                if '```' in cells[-1].content and n_previous_cells < len(cells):
                    p = cells[-1].content.index('```')
                    pre_text = text_utils.lstrip_text(cells[-1].content[:p], self.cell_symbol_start).strip()
                    if len(pre_text) > 0:
                        cells.insert(-2, Cell(content=f'{self.cell_symbol_start}\n{pre_text}\n{self.cell_symbol_end}', code_info=None))
                    cells[-1].content = f'{self.cell_symbol_start}\n{cells[-1].content[p:]}'

                    if not cells[-1].content.strip().endswith('```'):
                        cells[-1].content += '```\n'
                    activity_logger.info(f"start executing cell {len(cells)}")
                    tool_start_time = datetime.utcnow()
                    self.apply_tools(cells, legacy_memory, memory_manager)
                    duration_ms = round((datetime.utcnow() - tool_start_time).total_seconds() * 1000, 2)
                    activity_logger.info(f'cell {len(cells)} execution costs {duration_ms} ms')

                    # Below's code is to keep back compatibility: still support memory[-1]
                    if cells[-1].code_info is not None:
                        latest_code_result = cells[-1].code_info.code_execute_result
                        if isinstance(latest_code_result, SQLExecuteResult):
                            memory_obj = DefaultPlanner.convert_to_memory_obj(latest_code_result)
                            if memory_obj is not None:
                                legacy_memory.append(memory_obj)
                
                activity_logger.info(f"finish generating cells, iteration {iter_id}, generated {len(cells)} cells")
                yield cells   
                messages = messages_0.copy()
                messages.append(Message(role = MessageRole.ASSISTANT, content = f'{self.response_symbol_start}'))
                for i in range(0, len(cells)):
                    messages[-1].content += '\n'+cells[i].as_prompt_text(self.cell_symbol_start, self.cell_symbol_end, include_execution_result=False).strip()
                if n_previous_cells == len(cells):
                    break
                if cells[-1].code_info is None:
                    break
                result_text = ''
                if cells[-1].code_info and cells[-1].code_info.code_execute_result:
                    result_text = f"\n{cells[-1].code_info.code_execute_result.as_prompt_text()}".rstrip()
                messages.append(Message(role=MessageRole.USER,
                                        content=self.system_interrupt_message_template.format(result_text=result_text).strip()
                ))
            activity_logger.info(f"finish generating all cells, total iterations {iter_id}, total cells {len(cells)}")

    def should_stop(self, cells: List[Cell]):
        """
        Check whether the LLM should stop generating more cells.
        The last cell is an incomplete cell, which should be removed if should stop.

        1. Stop if the last cell is empty.
           The LLM is prompted to generate in the format of:
               <Response>
                   <Cell>...</Cell>
                   <Cell>...</Cell>
                   ...
                </Response>
            If the last cell is empty, it means that the LLM generates the </Response> symbol,
            thus it should stop generating more cells.
        2. Stop if the last cell does not follow the cell format.
           Each cell should be in the format of <Cell>...</Cell>,
               otherwise we should stop generating.
           As the last cell is incomplete,
               we should ensure that either it starts with <Cell> or <Cell> starts with it.
        """
        return len(cells[-1].content.strip()) == 0 or text_utils.lstrip_text(cells[-1].content.strip(), self.cell_symbol_start).strip().lower().startswith('the end') \
            or (
                len(cells) > 1
                    and
                not cells[-1].content.strip().startswith(self.cell_symbol_start)
                    and
                not self.cell_symbol_start.startswith(cells[-1].content.strip())
            )

    def apply_tools(self, cells: List[Cell], legacy_memory: List[Any], memory_manager: MemoryManager, **kwargs: Any) -> None:

        def get_code_result(code_id: str) -> CodeExecuteResult:
            code_id = str(code_id)
            code: CodeInfo = memory_manager.get_code(code_id)
            if code is None:
                # Current result has not been added into memory
                for prev_cell in cells[:-1]:
                    if prev_cell.code_info != None and prev_cell.code_info.code_id == code_id:
                        code = prev_cell.code_info

            if code is None:
                raise Exception(f"Code id {code_id} is invalid since it does not exist in current session. Let's generate all the required code from scratch.")
            
            code_result = code.code_execute_result
            if code_result is None and code.code_type in self.tool_dict:
                code_result = self.tool_dict[code.code_type].execute(code.code_block, cells=cells, get_code_result=get_code_result, memory=legacy_memory, **kwargs)
            
            if code_result is None:
                raise Exception(f"Can not find tool to execute the code {code_id}")
            
            if code_result.exception_message:
                raise Exception(f"Code id {code_id} gets execution exception {code_result.exception_message}. Let's fix and re-generate the code")
            
            code_result_obj = DefaultPlanner.convert_to_memory_obj(code_result)
            if code_result_obj is None:
                raise Exception(f"We can not get the result of code id {code_id}.")
        
            return code_result_obj

        cell = cells[-1]
        match = re.search(r'```(\w+)', cell.content)
        if match:
            tool_name = match.group(1)
            tool = self.tool_dict.get(tool_name, None)
            if tool:
                code = DefaultPlanner.extract_code(cell.content)
                if code:
                    # Not use LLM generated code_id
                    cell.code_info = CodeInfo(memory_manager.generate_unique_code_id(), tool_name, code, tool.execute(code, cells=cells, get_code_result=get_code_result, memory=legacy_memory))
    
    @staticmethod
    def extract_code(content: str) -> CodeBlock:
        regexes = [(r"```(\w+)\s+code_id='(\w+?)'\s+([\s\S]+?)```", 3), (r'```(\w+)\s+([\s\S]+?)```', 2)]
        for (regex, code_grp) in regexes:
            code_match = re.search(regex, content)
            if code_match:
                return CodeBlock(source=code_match.group(code_grp))
        
        return None

    @staticmethod
    def convert_to_memory_obj(code_execution_result: CodeExecuteResult) -> Any:        
        if isinstance(code_execution_result, SQLExecuteResult) and code_execution_result.data is not None:
            # TODO: to_pandas
            return DataFrame(code_execution_result.data.data, columns=code_execution_result.data.columns)
        
        if isinstance(code_execution_result, PythonExecuteResult) and code_execution_result.data is not None and isinstance(code_execution_result.data, dict):
            return json.dumps(code_execution_result.data)
        
        return None

    @property
    def prompt_text(self):
        prompt = ''
        params = {}
        for i, tool_item in enumerate(self.tool_dict.items()):
            tool_prompt = tool_item[1].prompt_text
            tool_key = f"tool_{i}"
            if isinstance(tool_prompt, str):
                params[tool_key] = StaticPromptComposer(tool_prompt)
            else:
                params[tool_key] = tool_prompt

            prompt += f'========= Tool {i+1}: {tool_item[0]} ========= \n{{{tool_key}}}\n\n'

        return CompoundPromptComposer(prompt, params)