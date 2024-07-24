from typing import Callable

from recursive_import import import_package_recursively

from thinking_tests.decorators import KNOWN_CASES
from thinking_tests.protocol import ThinkingCase
from thinking_tests.runner.protocol import BackendResultType
from thinking_tests.runner.run import execute
from thinking_tests.utils import root_pkg, caller_module_name


def default_sorter(cases: list[ThinkingCase]) -> list[ThinkingCase]:
    return sorted(cases, key=lambda x: x.coordinates)


def run_all(predicate: Callable[[ThinkingCase], bool] = None, *, root_package: str = "", sorter: Callable[[list[ThinkingCase]], list[ThinkingCase]] = None) -> BackendResultType:
    predicate = predicate or (lambda x: True)
    sorter = sorter or default_sorter
    if root_package is not None:
        import_package_recursively(root_package or root_pkg())
    return execute(sorter([x for x in KNOWN_CASES if predicate(x)]))

def run_current_module(predicate: Callable[[ThinkingCase], bool] = None, *, sorter: Callable[[list[ThinkingCase]], list[ThinkingCase]] = None) -> BackendResultType:
    predicate = predicate or (lambda x: True)
    sorter = sorter or default_sorter
    caller_module = caller_module_name(2) # 1 is this module, we're looking for caller of this method
    def final_predicate(x: ThinkingCase) -> bool:
        return x.coordinates.module_name == caller_module and predicate(x)
    return run_all(final_predicate, root_package=None, sorter=sorter)