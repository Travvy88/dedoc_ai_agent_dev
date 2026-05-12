# region MODULE_CONTRACT [DOMAIN(Testing): LDD; CONCEPT(Tests): TestUtilities; TECH(Python): Unittest, PDF]
## @modulecontract
## @purpose To provide shared test utilities for LDD-based tests: path resolution, config retrieval, line creation, tree traversal, and timeout control.
## @scope Test helper functions and classes for document structure verification.
## @input Test file paths, configuration, coordinate data.
## @output Resolved paths, test configs, LineWithLocation instances, tree nodes, linearized lines.
## @links [USES_API(8): dedoc.config, dedoc.data_structures, dedoc.readers; USES_API(6): dedocutils]
## @invariants
## - Tree traversal by path always returns a valid subtree dict.
## - Timeout alarm is cleared on context exit.
## @rationale
## Q: Why extract test utilities to a shared module?
## A: Multiple test files reuse line creation, config mockup, and tree helpers — centralizing avoids duplication.
## @changes
## LAST_CHANGE: [v1.0.0 – Added semantic template markup]
## @modulemap
## FUNC 4[Resolves test file paths] => get_full_path
## FUNC 5[Traverses tree by dotted path] => get_by_tree_path
## FUNC 3[Returns deep copy of config] => get_test_config
## FUNC 6[Creates LineWithLocation from coordinates] => create_line_by_coordinates
## FUNC 7[Linearizes tree to list] => tree2linear
## CLASS 6[Alarm-based test timeout] => TestTimeout
## @usecases
## - get_full_path: TestCase → ResolveFixturePath → FixtureLoaded
## - create_line_by_coordinates: TestCase → CreateMockLine → LineVerified
## - TestTimeout: TestCase → SetAlarm → CircuitBreaker
def _module_contract():
    pass
# endregion MODULE_CONTRACT
# GREP_SUMMARY: test utilities, LDD, line with location, tree traversal, test timeout, alarm, config mockup
# STRUCTURE: ▶ Init ┌test_utils┐ → ◇ get_full_path → ⊕ get_by_tree_path → ⚡ create_line_by_coordinates → ⟦TestTimeout⟧ → ∑ tree2linear → ⎋ utils ready

import os
import signal
from copy import deepcopy
from typing import Any, List, Optional, Union

from dedocutils.data_structures import BBox

from dedoc.config import get_config
from dedoc.data_structures.line_metadata import LineMetadata
from dedoc.readers.pdf_reader.data_classes.line_with_location import LineWithLocation
from dedoc.readers.pdf_reader.data_classes.tables.location import Location


def get_full_path(path: str, file: str = __file__) -> str:
    dir_path = os.path.dirname(file)
    return os.path.join(dir_path, path)


def get_by_tree_path(tree: dict, path: Union[List[int], str]) -> dict:
    if isinstance(path, str):
        path = [int(i) for i in path.split(".")][1:]
    for child_id in path:
        tree = tree["subparagraphs"][child_id]
    return tree


def get_test_config() -> dict:
    config = deepcopy(get_config())
    return config


def create_line_by_coordinates(x_top_left: int, y_top_left: int, width: int, height: int, page: int) -> LineWithLocation:
    bbox = BBox(x_top_left=x_top_left, y_top_left=y_top_left, width=width, height=height)
    location = Location(bbox=bbox, page_number=page)
    line = LineWithLocation(line="Some text", metadata=LineMetadata(page_id=page, line_id=0), annotations=[], location=location)
    return line


class TestTimeout:
    def __init__(self, seconds: int, error_message: Optional[str] = None) -> None:
        if error_message is None:
            error_message = f"tests timed out after {seconds}s."
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum: Any, frame: Any) -> None:  # noqa
        raise Exception(self.error_message)

    def __enter__(self) -> None:
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:  # noqa
        signal.alarm(0)


def tree2linear(tree: dict) -> List[dict]:
    lines = []
    stack = [tree]
    while len(stack) > 0:
        line = stack.pop()
        lines.append(line)
        stack.extend(line["subparagraphs"])
    lines.sort(key=lambda line: (line["metadata"]["page_id"], line["metadata"]["line_id"]))
    return lines
