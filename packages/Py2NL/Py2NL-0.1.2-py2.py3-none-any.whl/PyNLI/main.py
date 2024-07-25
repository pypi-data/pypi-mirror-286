from typing import Any

from .solara_interface import Page, Board, Chat, get_data_container, View

def NLICall(key: str = None, **kwargs) -> Any:
    data = get_data_container(key)
    data.vars.update(kwargs)
    for varname in kwargs:
        data.var_descriptions[varname] = 'Passed as parameter'


    return View(data)