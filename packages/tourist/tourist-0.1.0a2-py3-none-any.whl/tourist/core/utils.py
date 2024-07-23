import json

from dill.source import getsource


def to_single_line(script: str, as_json: bool = False) -> str:
    single_line = repr(script)[1:-1]
    single_line = json.dumps(single_line) if as_json else single_line
    return single_line.replace('"', r"\"").replace("'", r"\"")


def func_to_string(fn: callable, as_json: bool = False):
    source = getsource(fn)
    source += f"\n{fn.__name__}()\n"
    string = to_single_line(source, as_json)
    return string


def file_to_string(filename: str, as_json: bool = False):
    with open(filename, "r") as f:
        source = to_single_line(f.read(), as_json)
        return source
