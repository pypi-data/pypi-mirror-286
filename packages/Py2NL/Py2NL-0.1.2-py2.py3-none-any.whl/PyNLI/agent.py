import re
import threading
import time
from copy import copy
from queue import Queue
from typing import Union, Optional, Dict, Any, Tuple, List
import types

from langchain.agents import AgentOutputParser, ZeroShotAgent, AgentExecutor
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import CallbackManagerForChainRun, AsyncCallbackManagerForChainRun, Callbacks
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_core.utils import get_color_mapping
from pydantic import Field, BaseModel

from .prompts import get_agent_template, get_yes_no_template, get_detect_loop_template
from .sessions import st
from .config import default_config as config
from .tools import HumanTool, LookAtVariable, PythonConsoleTool, DESCRIPTION_HOOK_NAME


class OutputFormat(BaseModel):
    complete_command: str = Field(description='Rephrase the given task with additional info in natural language.')
    variable_name: str = Field(description='The name of the created or modified variables.')
    statement: str = Field(description='The statement about the result / the solution to the task.')


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str, inputs:Dict[str, str],intermediate_steps: List[Tuple[AgentAction, str]]) -> Union[AgentAction, AgentFinish]:
        prepend_code = ''
        ret = AgentAction(tool="empty", tool_input="", log=llm_output)
        pattern = re.compile(
            r"((?P<python>Python\s*\d*\s*Command\s*\d*\s*:)|(?P<show>Show\s*\d*\s*:)|(?P<thought>Thought\s*\d*\s*:)|(?P<question>Question\s*\d*\s*:)|(?P<solution>Final\s*\d*\s*Solution\s*\d*\s*:))[\s]*(?:(?!(Python\s*\d*\s*Command\s*\d*\s*:|Thought\s*\d*\s*:|Question\s*\d*\s*:|Final\s*\d*\s*Solution\s*\d*\s*:)).)*",
            re.DOTALL)
        for match in pattern.finditer(llm_output):
            text = match.group(0).split(':', 1)[1].strip()
            if match.group('thought'):
                prepend_code += f'# {text}\n'
            if match.group('question'):
                ret = AgentAction(tool="interact_with_human", tool_input={"query": text, 'inputs': copy(inputs), 'intermediate_steps': copy(intermediate_steps), 'store_in_history': True}, log=llm_output)
                ret.tool_input['current_step'] = ret
            if match.group('python'):
                code_match = re.search(r"(?<=```py\n).*(?=\n```)", text, re.DOTALL)
                text=code_match.group()
                ret = AgentAction(tool="execute_python_code", tool_input=prepend_code + text, log=llm_output)
            if match.group('show'):
                ret = AgentAction(tool="look_at_variable", tool_input=text, log=llm_output)
            if match.group('solution'):
                ret = AgentFinish(return_values={"output": text}, log=llm_output, )
                break

        return ret


def parse_variables(data, hide_description=False):
    s = ''
    for varname, var in data.vars.items():
        if varname not in [DESCRIPTION_HOOK_NAME]:
            if hide_description:
                s += f'| {varname} | {type(var).__name__} |\n'
            else:
                s += f'| {varname} | {type(var).__name__} | {data.var_descriptions.get(varname, "")} |\n'

    return s[:-1]

def set_variable_description(data, varname, description):
    data.var_descriptions[varname] = description


class AgentThread(threading.Thread):
    def __init__(self, key, args=(), kwargs=None):
        threading.Thread.__init__(self, args=args, kwargs=kwargs)
        self.query_queue = Queue()
        self.output_queue = Queue()
        self.daemon = True
        self.alive = True
        self.key = key

    def run(self):
        with get_openai_callback() as openai_stats:
            st.session_state[self.key].openai_stats = openai_stats
            while self.alive:
                query = '' if self.agent.reinit else self.query_queue.get()
                if query != '\\abort\\':
                    output = self.agent.invoke({'input': query})
                    if not self.agent.aborting:
                        self.output_queue.put({**output, 'store_in_history': True})

    def _get_tools(self):
        return [
            PythonConsoleTool(description_hook=st.session_state[self.key].set_variable_description),
            HumanTool(query_queue=self.output_queue, answer_queue=self.query_queue, key=self.key),
            LookAtVariable(key=self.key),
            Tool.from_function(lambda x: "", name="empty", description="does nothing"),
        ]

    def get_current_modules(self):
        module_names = list(self.agent.lookup_tool("execute_python_code").modules.keys())
        current_modules_text = ", ".join(module_names[:-1])
        if len(module_names) > 1:
            current_modules_text += " and "
        if len(module_names) >= 1:
            current_modules_text += module_names[-1]
        return current_modules_text

    def set_agent(self):
        def text_to_bool(inputs: dict) -> bool:
            return inputs['text'].lower() == "true"

        output_parser = CustomOutputParser()
        self.parser = PydanticOutputParser(pydantic_object=OutputFormat)

        st.session_state[self.key].parse_variables = types.MethodType(parse_variables, st.session_state[self.key])
        st.session_state[self.key].set_variable_description = types.MethodType(set_variable_description, st.session_state[self.key])

        tools = self._get_tools()
        agent_model = ChatOpenAI(temperature=0, model_name=config.agent_model_name)
        assistant_model = ChatOpenAI(temperature=0, model_name=config.assistant_model_name)

        st.session_state[self.key].python_console = tools[0]
        st.session_state[self.key].vars = st.session_state[self.key].python_console.locals
        st.session_state[self.key].var_descriptions = {}

        agent_chain = LLMChain(
            llm=agent_model,
            prompt=PromptTemplate(template=get_agent_template(), input_variables=["input"],
                                  partial_variables={"variables": st.session_state[self.key].parse_variables,
                                                     "modules": self.get_current_modules})
        )

        # final_solution_chain = LLMChain(
        #     llm=agent_model,
        #     prompt=PromptTemplate(template=get_prepare_final_solution_template(), input_variables=["input"],
        #                           partial_variables={"variables": parse_variables, "output_format": self.parser.get_format_instructions()})
        # )

        interpret_yes_no_chain = LLMChain(
            llm=assistant_model,
            prompt=PromptTemplate(template=get_yes_no_template(),
                                  input_variables=[])
        ) | text_to_bool

        detect_loop_chain = LLMChain(
            llm=assistant_model,
            prompt=PromptTemplate(template=get_detect_loop_template(),
                                  input_variables=["input", 'agent_scratchpad'])
        ) | text_to_bool

        agent_obj = CustomAgent(llm_chain=agent_chain,
                                tools=tools,
                                output_parser=output_parser)  # initialize_agent(tools, model, AgentType.OPENAI_FUNCTIONS)
        self.agent = CustomAgentExecutor(agent=agent_obj,
                                         tools=tools,
                                         key=self.key,
                                         callbacks=None,
                                         interpret_yes_no_chain=interpret_yes_no_chain,
                                         detect_loop_chain=detect_loop_chain,
                                         agent_output_format = self.parser.get_format_instructions(),
                                         max_iterations=config.max_iterations,
                                         return_intermediate_steps=True)


class CustomAgent(ZeroShotAgent):

    def plan(
        self,
        intermediate_steps: List[Tuple[AgentAction, str]],
        callbacks: Callbacks = None,
        **kwargs: Any,
    ) -> Union[AgentAction, AgentFinish]:
        """Given input, decided what to do.

        Args:
            intermediate_steps: Steps the LLM has taken to date,
                along with observations
            callbacks: Callbacks to run.
            **kwargs: User inputs.

        Returns:
            Action specifying what tool to use.
        """
        full_inputs = self.get_full_inputs(intermediate_steps, **kwargs)
        full_output = self.llm_chain.predict(callbacks=callbacks, **full_inputs)
        action = self.output_parser.parse(full_output, kwargs, intermediate_steps)
        return action

    def return_stopped_response(
        self,
        early_stopping_method: str,
        intermediate_steps: List[Tuple[AgentAction, str]],
        **kwargs: Any,
    ) -> AgentFinish:
        """Return response when agent has been stopped due to max iterations."""
        if early_stopping_method == "force":
            # `force` just returns a constant string
            return AgentFinish(
                {
                    "exeption" : "Agent stopped due to iteration limit.",
                    "output" : None
                }, "")
        else:
            raise ValueError(
                f"Got unsupported early_stopping_method `{early_stopping_method}`"
            )


class CustomAgentExecutor(AgentExecutor):

    inputs_override:Dict[str, str] = None
    intermediate_steps_init: List[Tuple[AgentAction, str]] = []
    current_step: AgentAction = None
    reinit: bool = False
    aborting:bool = False
    detect_loop_chain: LLMChain = None
    interpret_yes_no_chain: LLMChain = None
    confirmed: bool = False
    agent_output_format: str = ''
    key: str = None


    def __init__(self, agent, tools, key, callbacks, interpret_yes_no_chain, detect_loop_chain, agent_output_format, **kwargs):
        super(CustomAgentExecutor, self).__init__(agent=agent, tools=tools, callbacks=callbacks, **kwargs)
        self.interpret_yes_no_chain = interpret_yes_no_chain
        self.detect_loop_chain = detect_loop_chain
        self.agent_output_format = agent_output_format
        self.key = key


    def init(self, inputs:Dict[str, str], intermediate_steps:List[Tuple[AgentAction, str]], current_step:AgentAction):
        self.inputs_override = copy(inputs)
        self.intermediate_steps_init = copy(intermediate_steps)
        self.current_step = AgentAction(current_step.tool, current_step.tool_input, current_step.log)
        self.reinit = True

    def abort(self):
        self.aborting = True
        st.session_state[self.key].agent_thread.query_queue.put('\\abort\\')

    def _should_continue(self, iterations: int, time_elapsed: float) -> bool:
        return super()._should_continue(iterations, time_elapsed) and not self.aborting

    def _should_confirm(self, iterations: int, time_elapsed: float) -> bool:
        return not self.confirmed and iterations % config.iteration_confirmation_interval == 0

    def prep_inputs(self, inputs: Union[Dict[str, Any], Any]) -> Dict[str, str]:
        if not isinstance(inputs, dict):
            _input_keys = set(self.input_keys)
            if self.memory is not None:
                # If there are multiple input keys, but some get set by memory so that
                # only one is not set, we can still figure out which key it is.
                _input_keys = _input_keys.difference(self.memory.memory_variables)
            if len(_input_keys) != 1:
                raise ValueError(
                    f"A single string input was passed in, but this chain expects "
                    f"multiple inputs ({_input_keys}). When a chain expects "
                    f"multiple inputs, please call it by passing in a dictionary, "
                    "eg `chain({'foo': 1, 'bar': 2})`"
                )
            inputs = {list(_input_keys)[0]: inputs}
        if self.memory is not None:
            external_context = self.memory.load_memory_variables(inputs)
            inputs = dict(inputs, **external_context)
        inputs['final_solution_text'] = self.get_final_solution_text(inputs)
        self._validate_inputs(inputs)
        return inputs

    def _call(
        self,
        inputs: Dict[str, str],
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        """Run text through and get agent response."""
        # Construct a mapping of tool name to tool for easy lookup
        name_to_tool_map = {tool.name: tool for tool in self.tools}
        # We construct a mapping from each tool to a color, used for logging.
        color_mapping = get_color_mapping(
            [tool.name for tool in self.tools], excluded_colors=["green", "red"]
        )
        if self.inputs_override is not None:
            inputs = self.inputs_override
            self.inputs_override = None

        intermediate_steps: List[Tuple[AgentAction, str]] = self.intermediate_steps_init
        self.intermediate_steps_init = []

        # Let's start tracking the number of iterations and time elapsed
        iterations = len(intermediate_steps)
        time_elapsed = 0.0
        start_time = time.time()
        self.aborting = False
        self.confirmed = True
        # We now enter the agent loop (until it returns something).
        while self._should_continue(iterations, time_elapsed):
            while self._should_continue(iterations, time_elapsed) and not self._should_confirm(iterations, time_elapsed):
                self.confirmed = False
                if self.reinit:
                    agent_step = self._perform_agent_action(name_to_tool_map, color_mapping, self.current_step, run_manager)
                    next_step_output = [(agent_step.action, agent_step.observation)]
                    self.current_step = None
                    self.reinit = False
                else:
                    next_step_output = self._take_next_step(
                        name_to_tool_map,
                        color_mapping,
                        inputs,
                        intermediate_steps,
                        run_manager=run_manager,
                    )

                if isinstance(next_step_output, list) and next_step_output[0][0].tool == HumanTool.name:
                    interations = -1
                    self.confirmed = True

                if isinstance(next_step_output, AgentFinish):
                    if 'finalize' not in inputs:
                        inputs['finalize'] = True
                        inputs['final_solution_text'] = self.get_final_solution_text(inputs)
                        self.confirmed = True
                    else:
                        return self._return(inputs, next_step_output, intermediate_steps, run_manager=run_manager)
                else:
                    intermediate_steps.extend(next_step_output)

                    if len(next_step_output) == 1:
                        next_step_action = next_step_output[0]
                        # See if tool should return directly
                        tool_return = self._get_tool_return(next_step_action)
                        if tool_return is not None:
                            return self._return(inputs, tool_return, intermediate_steps, run_manager=run_manager)

                    iterations += 1
                    time_elapsed = time.time() - start_time

            progress_statement = 'I think I got stuck in a loop' if self.detect_loop_chain.invoke(self.agent.get_full_inputs(intermediate_steps, **inputs)) else 'I think I am still making progress'

            action = AgentAction(tool="interact_with_human",
                                 tool_input={"query": f'I have been working for {iterations} iterations and {progress_statement}. Should I continue?',
                                             'inputs': copy(inputs),
                                             'intermediate_steps': copy(intermediate_steps),
                                             'store_in_history': False},
                                 log=f"Total iterations until now: {iterations}")
            action.tool_input['current_step'] = action

            answer = self._perform_agent_action(name_to_tool_map, color_mapping, action, run_manager).observation

            self.confirmed = True

            answer_bool = self.interpret_yes_no_chain.invoke({'answer': answer})
            if not answer_bool:
                finish = AgentFinish(return_values={'output': '{"complete_command": "' + inputs['input'] + '", "variable_name": "", "statement": "The task has been aborted according to the users request."}'}, log="The task has been aborted according to the users request.")
                return self._return(inputs, finish, intermediate_steps, run_manager=run_manager)

        output = self.agent.return_stopped_response(
            self.early_stopping_method, intermediate_steps, **inputs
        )
        return self._return(inputs, output, intermediate_steps, run_manager=run_manager)


    def get_final_solution_text(self, inputs: Dict[str, str]) -> str:
        if 'finalize' in inputs:
            return f'the final solution to the Task. As final solution give the following output: {self.agent_output_format}'
        else:
            return 'the final solution to the Task has been reached.'

    def _return(
        self,
        inputs: Dict[str, str],
        output: AgentFinish,
        intermediate_steps: list,
        run_manager: Optional[CallbackManagerForChainRun] = None,
    ) -> Dict[str, Any]:
        final_output = super()._return(
                    output, intermediate_steps, run_manager=run_manager
                )
        final_output["inputs"] = inputs
        return final_output
