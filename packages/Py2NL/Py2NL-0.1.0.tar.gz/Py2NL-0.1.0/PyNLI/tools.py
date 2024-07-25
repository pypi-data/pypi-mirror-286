import ast
import warnings
from queue import Queue
from types import NoneType
from typing import Optional, Dict, Tuple, List

from sessions import st
from langchain_core.agents import AgentAction
from langchain_core.callbacks import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_experimental.tools import PythonAstREPLTool

import libcst as cst

DESCRIPTION_HOOK_NAME = 'hook_update_variable_description'


class DescriptionHookInserter(cst.CSTTransformer):
    def leave_SimpleStatementLine(self, old_node, updated_node):
        if isinstance(updated_node.body[0], cst.Assign) and isinstance(updated_node.body[0].targets[0].target,
                                                                       cst.Name):
            varname = updated_node.body[0].targets[0].target.value
            description = ''
            if updated_node.trailing_whitespace.comment is not None:
                description = updated_node.trailing_whitespace.comment.value[1:].strip()

            log_stmt = cst.parse_module(f"{DESCRIPTION_HOOK_NAME}('{varname}', '{description}')").body
            return cst.FlattenSentinel([*log_stmt, updated_node])
        return updated_node


class PythonConsoleTool(PythonAstREPLTool):
    name = "execute_python_code"
    description = "executes code as a python file."
    history = []
    modules = {}

    description_hook: NoneType = None

    def __init__(self, description_hook):
        super().__init__()
        self.description_hook = description_hook

    def add_module(self, import_statement: str, module_name: str = None, description: str = None):
        tree = ast.parse(import_statement)
        if len(tree.body) == 1:
            if isinstance(tree.body[0], (ast.Import, ast.ImportFrom)):
                import_node = tree.body[0]
                if len(import_node.names) == 1:
                    alias = import_node.names[0]
                    if module_name is None:
                        module_name = alias.name
                    elif not isinstance(module_name, str):
                        warnings.warn("module_name is not a string and will be ignored")
                        module_name = alias.name
                    python_name = alias.name if alias.asname is None else alias.asname
                else:
                    warnings.warn(f"```\n{import_statement}\n```\nimports multiple things at once which is not allowed and will not be executed")
                    return
            else:
                warnings.warn(f"```\n{import_statement}\n```\nthe code is not an import and will not be executed")
                return
        else:
            warnings.warn(f"```\n{import_statement}\n```\nthe code may only contain a single import which is not the case. It will not be executed")
            return

        if description is None:
            import_statement += f" # {python_name}: the {module_name} module"
        else:
            import_statement += f" # {python_name}: {description}"
            if module_name not in description:
                warnings.warn(f"the description of the module '{module_name}' does not contain the module name. Description: {description}")

        if module_name in self.modules:
            warnings.warn(f"a module named '{module_name}' already exists. the import will not be executed")
            return
        else:
            self.modules[module_name] = import_statement

    def remove_module(self, module_name):
        if module_name in self.modules:
            tree = ast.parse(self.modules.pop(module_name))
            alias = tree.body[0].names[0]
            python_name = alias.name if alias.asname else alias.asname
            super()._run(f"del {python_name}")
        else:
            print(f"no module named {module_name} is imported")

    def start_new_period(self):
        self.history.append([])

    def validate(self, query: str):
        error = []
        tree = ast.parse(query)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                error.append('import is forbidden.')
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'open':
                error.append('open() is forbidden.')
        if len(error) == 0:
            return None
        else:
            return '\n'.join(sorted(set(error)))

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        if DESCRIPTION_HOOK_NAME not in self.locals:  # heuristic for testing if console was correctly initialized
            self.locals[DESCRIPTION_HOOK_NAME] = self.description_hook
        for module_name in self.modules:
            import_statement_cst = cst.parse_module(self.modules[module_name])
            import_statement = import_statement_cst.visit(DescriptionHookInserter()).code
            print(import_statement)
            super()._run(import_statement)

        error = self.validate(query)
        if error is not None:
            return error

        self.history[-1].append(query)

        query_cst = cst.parse_module(query)
        query = query_cst.visit(DescriptionHookInserter()).code

        reply = super()._run(query, run_manager)

        if isinstance(reply, str):
            splitreply = reply.split(":")
            if len(splitreply) > 1 and (
                    splitreply[0].endswith("Error") or splitreply[0].endswith("Exception") or splitreply[0].endswith(
                    "Interrupt")):
                self.history[-1].pop()

        return reply

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        error = self.validate(query)
        if error is not None:
            return error

        self.history[-1].append(query)
        reply = super()._arun(query, run_manager)
        if isinstance(reply, str):
            splitreply = reply.split(":")
            if len(splitreply) > 1 and (
                    splitreply[0].endswith("Error") or splitreply[0].endswith("Exception") or splitreply[0].endswith(
                "Interrupt")):
                self.history[-1].pop()
        return reply

    def validate_only_run (
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        error = self.validate(query)
        if error is not None:
            return error

        reply = super()._run(query, run_manager)

        return reply

    def avalidate_only_run(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        error = self.validate(query)
        if error is not None:
            return error

        reply = super()._arun(query, run_manager)

        return reply

class HumanTool(BaseTool):
    name = "interact_with_human"
    description = "asks the human for feedback"

    query_queue: Queue
    answer_queue: Queue
    key: str

    def _run(
            self, query: str, inputs:Dict[str, str], intermediate_steps: List[Tuple[AgentAction, str]], current_step: AgentAction, store_in_history: bool = True, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        if not st.session_state[self.key].agent_thread.agent.reinit:
            self.query_queue.put({'question': query, 'inputs': inputs, 'intermediate_steps': intermediate_steps, 'current_step': current_step, 'store_in_history': store_in_history})
        reply = self.answer_queue.get()
        return reply

    async def _arun(
            self, query: str, inputs:Dict[str, str], intermediate_steps: List[Tuple[AgentAction, str]], current_step: AgentAction, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        if not st.session_state[self.key].agent_thread.agent.reinit:
            self.query_queue.put({'question': query, 'inputs': inputs, 'intermediate_steps': intermediate_steps, 'current_step': current_step})
        reply = self.answer_queue.get()
        return reply


class LookAtVariable(BaseTool):
    name = "look_at_variable"
    description = "gets the value of the given variable"
    key: str

    # def __init__(self, python_console_tool: PythonConsoleTool):
    #     self.python_console_tool = python_console_tool

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        reply_list = []
        varnames = [part.strip() for part in query.split(",")]
        for varname in varnames:
            if varname not in st.session_state[self.key].vars:
                tree = ast.parse(varname)
                if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value,
                                                                                             ast.Name):
                    reply_list.append(f'\"{varname}\" is not defined.')
                else:
                    reply_list.append(f'\"{varname}\" is not a variable. Create a variable for this first.')
            else:
                reply_list.append(f"{varname}:\n{st.session_state[self.key].vars[varname]}")

        return "\n\n".join(reply_list)

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        reply_list = []
        varnames = [part.strip() for part in query.split(",")]
        for varname in varnames:
            if varname not in st.session_state[self.key].vars:
                reply_list.append(f'\"{varname}\" is not defined.')
            else:
                reply_list.append(f"{varname}:\n{st.session_state[self.key].vars[varname]}")

        return "\n\n".join(reply_list)