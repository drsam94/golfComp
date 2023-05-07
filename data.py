from enum import Enum 
from typing import Iterable, Tuple, Optional

class Language(Enum):
    Python = 1
    Cpp = 2
    C = 3

class ProblemStatement:
    def __init__(self, name: str, test_inputs: Iterable[Tuple]):
        self.name = name
        self.test_inputs = test_inputs

class TestResult:
    def __init__(self, size=0, err: Optional[str] = None, time=0.):
        self.size = size
        self.err = err
        self.time = time

    def __str__(self):
        if self.err:
            return f"ERROR: {self.err}"
        else:
            return f"SUCCESS: {self.size} (time {self.time}s)"

