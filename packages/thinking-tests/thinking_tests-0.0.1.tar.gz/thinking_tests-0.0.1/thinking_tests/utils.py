import inspect
import sys
from os.path import join, exists

from recursive_import import _abs_dirname

def main_module():
    return sys.modules["__main__"]

def root_pkg(path: str = None) -> str:
    abs_path = _abs_dirname(path or main_module().__file__)
    shallowest_module = None
    while exists(join(abs_path, "__init__.py")):
        abs_path, slash, shallowest_module = abs_path.rpartition("/")
    assert shallowest_module is not None
    return shallowest_module

def caller_module_name(lvl=1):
    """
    :param lvl: 0 - refers to invocation of caller_module_name itself, will return name of this module;
    1 - who called this method?;
    -1 - main function running this interpreter
    :return: module name, possibly "__main__"
    """
    s = inspect.stack() # 0 -
    return s[lvl].frame.f_globals["__name__"]
