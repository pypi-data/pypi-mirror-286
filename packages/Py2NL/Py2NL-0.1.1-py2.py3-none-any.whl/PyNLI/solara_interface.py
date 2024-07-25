import builtins
import os
import pickle
import sys
import threading
from copy import copy
from pathlib import Path
import asyncio
import markdown
import langchain
import openai
import pandas as pd
import solara
import solara.lab
from typing import List, Any as T

from solara.components.file_drop import FileInfo

from config import default_config as config
from sessions import st, DataContainer
from extraction import extract_function, get_occurrences
from agent import AgentThread, parse_variables
from messages import *

#%%
def get_data_container(key):

    langchain.debug = True

    if key not in st.session_state:
        st.session_state[key] = DataContainer()
        st.session_state[key].key = key

    if 'messages' not in st.session_state[key]:
        st.session_state[key].messages = []
    if 'code' not in st.session_state[key]:
        st.session_state[key].code = ""
    if "tabla_of_variables" not in st.session_state[key]:
        st.session_state[key].table_of_variables = ""
    if 'agent_thread' not in st.session_state[key]:
        st.session_state[key].agent_thread = AgentThread(key=key)
        # add_script_run_ctx(st.session_state[key].agent_thread)
        st.session_state[key].agent_thread.set_agent()
        st.session_state[key].agent_thread.start()
    if "module_checkbox_values" not in st.session_state[key]:
        st.session_state[key].module_import_statements = {}
        st.session_state[key].module_checkbox_values = {}
    if 'force_update' not in st.session_state[key]:
        st.session_state[key].force_update = Multicast()
    if "chat_width" not in st.session_state[key]:
        st.session_state[key].chat_width = solara.Reactive(0.5)
    if "function" not in st.session_state[key]:
        st.session_state[key].function = solara.Reactive(None)
        st.session_state[key].occurrences = solara.Reactive([])
        st.session_state[key].inputs = solara.Reactive([])
        st.session_state[key].outputs = solara.Reactive([])

    return st.session_state[key]


def update_module_state(data, module_name):
    if data.module_checkbox_values[module_name].value:
        data.python_console.add_module(data.module_import_statements[module_name], module_name)
    else:
        data.python_console.remove_module(module_name)

def refresh_board():
    st.session_state.table_of_variables = f"""| Variable Name | Datatype | Description |
| --- | --- | --- |
{parse_variables(hide_description=False)}"""
    st.session_state.code = '\n'.join(["\n".join(period) for period in st.session_state.python_console.history])

    # board_emptyable.empty()
    # with board_emptyable.container():
    #     if "openai_stats" in st.session_state:
    #         st.write(st.session_state.openai_stats)
    #     st.markdown(st.session_state.table_of_variables)
    #     st.divider()
    #     st.code(st.session_state.code, line_numbers=True)


def add_rollback_button(chat_message, index):
    def undo_chat():
        st.session_state.messages = st.session_state.messages[:index]
        st.session_state.python_console._run("reset -f")
        st.session_state.python_console.history = []
        # st.session_state.vars = st.session_state.python_console.locals
        for message in st.session_state.messages:
            if "file" in message or "exception" in message:
                continue

            st.session_state.python_console.start_new_period()
            for snipet in message['code']:
                st.session_state.python_console._run(snipet)

        for i in reversed(range(len(st.session_state.messages))):
            if 'AI-response' in st.session_state.messages[i]:
                if "question" in st.session_state.messages[i]["AI-response"]:
                    st.session_state.agent_thread.agent.init(st.session_state.messages[i]["AI-response"]["inputs"],
                                                             st.session_state.messages[i]["AI-response"]["intermediate_steps"],
                                                             st.session_state.messages[i]["AI-response"]["current_step"])

                break

        st.session_state.agent_thread.agent.abort()

    with chat_message:
        st.button('Rollback', key=f'rollback_{index}', on_click=undo_chat)


def load_files(data, files: List[FileInfo]):
    def load_data_file(file: FileInfo):
        file['file_obj'].seek(0)
        if file['name'].endswith(".csv"):
            filedata = pd.read_csv(file['file_obj'] if config.lazy_files else file['data'])
            description = 'the dataframe of a CSV-file'
            varname = file['name'].split('.')[0]
            data.vars[varname] = filedata
            data.var_descriptions[varname] = description
        elif file['name'].endswith((".xls", ".xlsx")):
            filedata = pd.read_excel(file['file_obj'] if config.lazy_files else file['data'])
            description = 'Contains a dataframe for each sheet of an Excel-file'
            varname = file['name'].split('.')[0]
            data.vars[varname] = filedata
            data.var_descriptions[varname] = description
        else:
            solara.Info("Only .csv, .xls/xlsx or .chat can be loaded")

    chat_file = None
    for file in files:
        if file['name'].endswith(".chat"):
            if chat_file:
                solara.Info(f"multiple .chat files found! {file['name']} will be ignored. {chat_file['name']} will be loaded.")
            else:
                chat_file = file

    if chat_file:
        data.messages = pickle.load(chat_file['file_obj']) if config.lazy_files else pickle.loads(file['data'])
        data.python_console.start_new_period()
        data.python_console._run("reset -f")
        data.python_console.history = []
        last_AIMessage = None
        for message in data.messages:
            if isinstance(message, SystemMessage):
                if "file" in message:
                    load_data_file(message["file"])
                    continue

            elif isinstance(message, AIMessage):
                last_AIMessage = message
                data.python_console.start_new_period()
                for snipet in message['code']:
                    data.python_console._run(snipet)

        if last_AIMessage is not None and "question" in last_AIMessage:
            data.agent_thread.agent.init(last_AIMessage["inputs"],
                                         last_AIMessage["intermediate_steps"],
                                         last_AIMessage["current_step"])

            data.agent_thread.agent.abort()

    data.force_update()

    for file in files:
        if not file['name'].endswith(".chat"):
            data.messages.append(SystemMessage(file=file))
            load_data_file(file)
            data.force_update()


def make_module_checkbox(data, module_name, import_statement):
    initilalize = True
    if module_name in data.module_checkbox_values:
        initilalize = False

    if initilalize:
        data.module_checkbox_values[module_name] = solara.Reactive(True)
        data.module_import_statements[module_name] = import_statement
        update_module_state(data, module_name)

    return solara.Checkbox(label=module_name, value=data.module_checkbox_values[module_name], on_value=lambda state: update_module_state(data, module_name))


def extract_function_and_display(data):
    inputs = [input[:2] for input in data.inputs.value]
    outputs = [output[:2] for output in data.outputs.value]
    imports = '\n'.join(data.module_import_statements.values())
    all_inputs, extracted_function = extract_function(f'{imports}\n{data.code}', data.key, inputs, outputs)
    data.function.value = DataContainer(code=extracted_function, callable=0)
    complied = compile(extracted_function, '', 'exec')
    exec(complied, sys.modules["__main__"].__dict__)

class Multicast:
    delegates = []

    def __call__(self, *args, **kwargs):
        for delegate in self.delegates:
            delegate(*args, **kwargs)

    def __contains__(self, item):
        return item in self.delegates

    def add(self, other):
        if isinstance(other, Multicast):
            self.delegates.extend(other.delegates)
        else:
            self.delegates.append(other)

    def remove(self, other):
        if isinstance(other, Multicast):
            for delegate in other.delegates:
                self.delegates.remove(delegate)
        else:
            self.delegates.remove(other)

#%%

@solara.component
def CodeBlock(code: str, line_numbers: bool = False, language: str = "plaintext"):
    def make_markdown_object():
        def highlight(src, language, *args, **kwargs):
            try:
                return solara.components.markdown._highlight(src, language, False, *args, **kwargs)
            except Exception as e:
                solara.components.markdown.logger.exception("Error highlighting code: %s", src)
                return repr(e)

        if solara.components.markdown.has_pymdownx:
            return markdown.Markdown(  # type: ignore
                extensions=[
                    "pymdownx.highlight",
                    "pymdownx.superfences",
                    "pymdownx.emoji",
                    "toc",  # so we get anchors for h1 h2 etc
                    "tables",
                ],
                extension_configs={
                    "pymdownx.emoji": {
                        "emoji_index": solara.components.markdown._no_deep_copy_emojione,
                    },
                    "pymdownx.superfences": {
                        "custom_fences": [
                            {
                                "name": "mermaid",
                                "class": "mermaid",
                                "format": solara.components.markdown.pymdownx.superfences.fence_div_format,
                            },
                            {
                                "name": "solara",
                                "class": "",
                                "format": highlight,
                            },
                        ],
                    },
                },
            )
        else:
            solara.components.markdown.logger.warning("Pymdownx not installed, using default markdown. For a better experience, install pymdownx.")
            return markdown.Markdown(  # type: ignore
                extensions=[
                    "fenced_code",
                    "codehilite",
                    "toc",
                    "tables",
                ],
            )

    md = solara.use_memo(make_markdown_object)
    code_html = md.convert(f'```{language}\n{code}\n```')
    code_html_lines = code_html[28:-12].splitlines(True)
    html = f'<pre><ol><li>{"</li><li>".join(code_html_lines[:-1])}{code_html_lines[-1]}</li></ol></pre>' if line_numbers else f'<pre>{"".join(code_html_lines)}</pre>'

    return solara.HTML('div', unsafe_innerHTML=html, classes=['highlight'])


@solara.component
def Select(data: DataContainer, label='Show options', selected: List[T] | solara.Reactive[List[T]] = [], options: List[T] | solara.Reactive[List[T]] = [], format_fn=str):
    is_initialized, set_is_initialized = solara.use_state(False)
    counter, set_counter = solara.use_state(0)

    def force_update():
        set_counter(lambda counter: counter+1)

    if not is_initialized:
        data.force_update.add(force_update)

    selected = solara.use_reactive(selected)
    options = solara.use_reactive(options)
    filtered = solara.use_reactive(options.value)

    def toggle(option):
        if option in selected.value:
            selected.value.remove(option)
        else:
            selected.value.append(option)

        force_update()

    def filter_options(text):
        filtered.value = [option for option in options.value if text in format_fn(option)]

    btn = solara.Button(label)
    with solara.lab.Menu(activator=btn, close_on_content_click=False):
        solara.InputText("Filter:", on_value=filter_options, continuous_update=True)
        with solara.Column(gap="0px"):
            for option in filtered.value:
                solara.Button(format_fn(option), on_click=(lambda o: lambda: toggle(o))(option), text=True, color='primary' if option in selected.value else None)
            if len(filtered.value) == 0:
                solara.Text('No options')

    set_is_initialized(True)


@solara.component
def Board(data: DataContainer):
    is_initialized, set_is_initialized = solara.use_state(False)
    counter, set_counter = solara.use_state(0)

    def force_update():
        set_counter(lambda counter: counter+1)

    if not is_initialized:
        data.force_update.add(force_update)

    with solara.Column() as board:
        load_progress, set_load_progress = solara.use_state(.0)

        solara.FileDropMultiple(on_file=lambda new_files: asyncio.run(asyncio.to_thread(load_files, data, new_files)), on_total_progress=lambda progress: set_load_progress(progress), lazy=config.lazy_files)
        solara.ProgressLinear(load_progress)

        solara.Markdown("**libraries to work with:**")
        make_module_checkbox(data, "pandas", "import pandas as pd")
        make_module_checkbox(data, "NumPy", "import numpy as np")
        make_module_checkbox(data, "OpenCV", "import cv2 as cv")
        make_module_checkbox(data, "Pillow", "import PIL")

        solara.FileDownload(data=lambda: pickle.dumps(data.messages), filename=f'{data.key}.chat', label='Download Session')


        data.table_of_variables = f"""| Variable Name | Datatype | Description |
| --- | --- | --- |
{parse_variables(data, hide_description=False)}"""

        solara.Markdown(data.table_of_variables)

        with solara.Card():
            solara.display(data.openai_stats)

        data.code = '\n'.join(["\n".join(period) for period in data.python_console.history if len(period) > 0])

        CodeBlock(data.code, line_numbers=True, language='python')

        name_index, line_index = 0, 1
        Select(data,"Pick inputs", data.inputs, data.occurrences, lambda occurrence: f'{occurrence[name_index]} | line: {occurrence[line_index]}')
        Select(data,"Pick outputs", data.outputs, data.occurrences, lambda occurrence: f'{occurrence[name_index]} | line: {occurrence[line_index]}')
        solara.Button("Create function", on_click=lambda: extract_function_and_display(data))

        def update_occurrences():
            (name_index, line_index, usage_index, _, _), occurrences_by_name = get_occurrences(data.code, return_usage=True,
                                                                                               only_strongest_usage=True,
                                                                                               prepend_name=True)
            data.occurrences.value.clear()
            for name in occurrences_by_name:
                data.occurrences.value.extend(occurrences_by_name[name])

        if not is_initialized:
            data.force_update.add(update_occurrences)

        update_occurrences()

        if data.function.value is not None:
            CodeBlock(data.function.value["code"], True, 'python')

    set_is_initialized(True)

    return board

@solara.component
def Chat(data: DataContainer):
    is_initialized, set_is_initialized = solara.use_state(False)
    counter, set_counter = solara.use_state(0)

    def force_update():
        set_counter(lambda counter: counter+1)

    if not is_initialized:
        data.force_update.add(force_update)

    user_message_count = len([message for message in data.messages if isinstance(message, HumanMessage)])

    def send(message):
        append_message(HumanMessage(content=message))

    def append_message(message):
        data.messages.append(message)
        force_update()

    async def process_user_message():
        if user_message_count == 0 or not isinstance(data.messages[-1], HumanMessage):
            return

        if 'temporary_message' not in data:
            data.python_console.start_new_period()

        data.agent_thread.query_queue.put(data.messages[-1].content)

        if 'temporary_message' in data:
            message = data.temporary_message
            del data.temporary_message

        #append_message(HumanMessage(content=message))

        output = data.agent_thread.output_queue.get()

        if output['store_in_history']:
            del output['store_in_history']

            #add_rollback_button(human_message, len(data.messages) - 1)
        else:
            data.temporary_message = message

        append_message(AIMessage(**output, code=data.python_console.history[-1]))

        data.force_update()


    task = solara.lab.use_task(process_user_message, dependencies=[user_message_count])


    with solara.Column(
            style={"width": "100%", "height": "100%", 'padding': '40px'},
    ):
        with solara.lab.ChatBox():
            for i, message in enumerate(data.messages):
                if isinstance(message, HumanMessage):
                    with solara.lab.ChatMessage(
                            user=True,
                            avatar=False,
                            name="User",
                            color="#ff991f",
                            avatar_background_color=None,
                            border_radius="10px",
                    ):
                        solara.Markdown(message.content)
                        solara.Button(f'Rollback')

                elif isinstance(message, AIMessage):
                    with solara.lab.ChatMessage(
                            user=False,
                            avatar=False,
                            name="Assistant",
                            color="rgba(0,0,0, 0.06)",
                            avatar_background_color="primary",
                            border_radius="10px",
                    ):
                        if 'exception' in message:
                            solara.Error(message['exception'])
                        elif 'question' in message:
                            solara.Markdown(message['question'])
                        else:
                            parsed = data.agent_thread.parser.parse(message['output'])

                            solara.Markdown(parsed.complete_command)
                            solara.Markdown(parsed.statement)

                            with solara.lab.Tabs(1):
                                varnames = [part.strip() for part in parsed.variable_name.split(",")]
                                if len(varnames) > 0:
                                    solara.lab.Tab()
                                for varname in varnames:
                                    if varname in data.vars:
                                        with solara.lab.Tab(varname):
                                            if isinstance(data.vars[varname], str) and len(data.vars[varname]) > 1500:
                                                solara.Markdown(f'{data.vars[varname][:1500]}[...]')
                                            else:
                                                solara.display(data.vars[varname])

        if task.pending:
            solara.ProgressLinear()
        solara.lab.ChatInput(send_callback=send, disabled=task.pending)

    set_is_initialized(True)


def make_chat(key):
    data = get_data_container(key)
    chat = Chat(data)
    return chat

@solara.component
def View(data: DataContainer):
    with solara.AppBar():
        with solara.Column(style="width: 100%"):
            solara.SliderFloat("Split position", data.chat_width, min=0, max=1, step=0.01)

    if data.chat_width.value == 0:
        Board(data)
    elif data.chat_width.value == 1:
        Chat(data)
    else:
        with solara.Columns([data.chat_width.value,1-data.chat_width.value]):
            Chat(data)
            Board(data)

@solara.component
def Page():
#     solara.Style(Path('webstuff/styles.css'))
#     solara.HTML(unsafe_innerHTML='''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css">
# <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
#
# <script>hljs.highlightAll();</script>''')
    data = get_data_container("func")

    return View(data)

