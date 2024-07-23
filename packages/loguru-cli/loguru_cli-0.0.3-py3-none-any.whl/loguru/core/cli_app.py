import random
import traceback

from langchain_community.llms.ollama import Ollama
from langchain_core.messages import AIMessage
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from prettytable import PrettyTable

from loguru.core.fs_log_rag import LoguruRAG
from loguru.core.history_manager import CommandHistoryManager
from loguru.core.models.config import Config

import sys


class CLIApp:
    def __init__(self, config: Config, with_tools=False, tool_registry: [] = None):
        self._config = config
        self._history_mgr = CommandHistoryManager()
        self._with_tools = with_tools
        self._tool_registry = tool_registry
        if with_tools:
            # print("Using tools...")
            pass
        else:
            # print("Using raw mode...")
            pass

    # noinspection PyMethodMayBeStatic
    def _call_tools(self, query: str, model: str, base_url: str, stream: bool = False):
        """
        Make sure to use model 'mistral' for this capability

        :param query:
        :param model:
        :param base_url:
        :param stream:
        :return:
        """
        llm = OllamaFunctions(model=model, base_url=base_url, format="json", temperature=0)
        llm_with_tools = llm.bind_tools(self._tool_registry)
        try:
            # noinspection PyTypeChecker
            response: AIMessage = llm_with_tools.invoke(query)
            if len(response.tool_calls) > 0:
                for tool_call in response.tool_calls:
                    function_name = tool_call['name']
                    function_args = tool_call['args']

                    kwargs_str = ", ".join(f"{key}={repr(value)}" for key, value in function_args.items())
                    eval_statement = f"{function_name}({kwargs_str}).run(config={self._config.dict()}, user_query='{query}')"
                    # print(eval_statement)
                    # print("Calling function: " + eval_statement)
                    # TODO: replace string imports with Pythonic form
                    exec(
                        f'from loguru.core.tool_impls import *;from loguru.core.models.config import *;{eval_statement}')
            else:
                print("Could not process the query.")
                # self._ask_llm_raw(query, model, base_url, stream=True)
        except Exception as e:
            print("Oops, seems like the AI cannot process that!")
            print(e)
            # traceback.print_exc(file=sys.stdout)

    # noinspection PyMethodMayBeStatic

    def _llm_interact(self, input_text: str, with_tools: bool = False, stream: bool = False):
        try:
            if with_tools:
                self._call_tools(
                    query=input_text,
                    model=self._config.ollama.llm_name,
                    base_url=str(random.choice(self._config.ollama.hosts)),
                    stream=False
                )
            else:
                self._ask_llm_raw(
                    query=input_text,
                    stream=False
                )
        except Exception as e:
            print("Oops, we hit a snag!")
            # TODO: Write to log file and prettify the error that user can see
            print(f"Error: {e}")
            traceback.print_exc(file=sys.stdout)

    def _ask_llm_raw(self, query: str, stream: bool = True):
        lg = LoguruRAG(config=self._config)
        lg.scan()
        resp = lg.ask(question=query, stream=stream)

    def scan_and_rebuild_cache(self):
        LoguruRAG(config=self._config).scan(clean_and_rebuild=True)

    def start(self):
        from prompt_toolkit import prompt
        from prompt_toolkit.styles import Style
        from prompt_toolkit.shortcuts import CompleteStyle
        from prompt_toolkit.formatted_text import HTML

        _prompt_style = Style.from_dict({
            'placeholder': '#FF0000',  # Light gray color for the placeholder
        })

        def _get_user_input():
            prompt_text = '>>> '
            prompt_placeholder = 'Enter your query here (/? for help)'
            return prompt(
                prompt_text,
                # placeholder='Enter your query here (/? for help)',
                placeholder=HTML(f'<ansigray>{prompt_placeholder}</ansigray>'),
                default='',
                complete_style=CompleteStyle.READLINE_LIKE,
                style=_prompt_style
            )

        def _show_help():
            _cmd_help_dict = {
                '/?': 'Show this help',
                '/history': 'Show history',
                '/bye': 'Exit'
            }
            cols = ["Command", "Description"]
            t = PrettyTable(cols)
            t.align[cols[0]] = "l"
            t.align[cols[1]] = "l"
            for k in _cmd_help_dict:
                t.add_row([k, _cmd_help_dict[k]])
            print(t)

        while True:
            user_input = _get_user_input()
            if user_input == '/bye':
                print('Exiting...')
                break
            elif user_input == '/?':
                _show_help()
            elif user_input == '/history':
                self._history_mgr.print()
            elif user_input.strip() == '':
                continue
            else:
                self._history_mgr.record(command=user_input)
                self._llm_interact(
                    input_text=user_input,
                    with_tools=self._with_tools  # Change to False for raw LLM response
                )
