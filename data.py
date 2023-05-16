from enum import Enum 
from typing import Iterable, Tuple, Optional

class Language(Enum):
    Python = 1
    Cpp = 2
    C = 3
    Javascript = 4
    APL = 5

    @staticmethod
    def from_ext(ext: str):
        if ext == ".py":
            return Language.Python 
        elif ext in [".cc", ".cpp"]:
            return Language.Cpp
        elif ext == ".c":
            return Language.C
        elif ext == ".js":
            return Language.Javascript
        elif ext == ".apl":
            return Language.APL 
        else:
            return None

class ProblemStatement:
    def __init__(self, name: str, test_inputs: Iterable[Tuple]):
        self.name = name
        self.test_inputs = test_inputs

class TestResult:
    def __init__(self, *, lang: Optional[Language]=None,size=0, err: Optional[str] = None, time=0.):
        self.size = size
        self.err = err
        self.time = time
        self.lang = lang

    def is_valid(self) -> bool:
        return not self.err
    
    def __str__(self):
        if not self.is_valid():
            return f"ERROR: {self.err}"
        else:
            return f"SUCCESS: {self.size} (time {self.time}s)"

