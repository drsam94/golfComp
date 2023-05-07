#!/usr/bin/python3
# Python 3.9.2

import sys
from pathlib import Path 
from typing import Optional, Dict, List, Any, Tuple, Iterable, Generator
from abc import ABC, abstractmethod
from enum import Enum

class Language(Enum):
    Python = 1
    Cpp = 2

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

class Executor(ABC):
    @abstractmethod 
    def __init__(self, filename: Path):
        """
        Initialize the executor and do any preprocessing on the file to get ready to execute
        (e.g import a python module or compile an external language)
        """
        ...
    
    @abstractmethod
    def execute(self, args: Tuple) -> Any:
        """
        Take an input argument and compute the output. We haven't fully defined the universe of inputs
        and outputs and how they should be passed, but probably everything is an int or a str
        """
        ...

class PythonExecutor(Executor):

    def __init__(self, filename: Path):
        import importlib.util
        module_name = "test.golf"
        spec = importlib.util.spec_from_file_location(module_name, filename)
        assert spec
        self.test_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = self.test_module
        spec.loader.exec_module(self.test_module) # type: ignore

    def execute(self, args: Tuple) -> Any:
        return self.test_module.ans(*args) # type: ignore
    
def make_executor(lang: Language, filename: Path) -> Executor:
    if lang != Language.Python:
        raise Exception("Unsupported")
    return PythonExecutor(filename)

def wrap_in_tuple(input: Iterable[Any]) -> Iterable[Any]:
    for elem in input:
        yield (elem,)

def problem_list() -> List[ProblemStatement]:
    ret = []
    ret.append(ProblemStatement("test1", wrap_in_tuple(list(range(10)) + [25, 45, 1000, 10000, 99999])))
    ret.append(ProblemStatement("test2", [
        (1900, 1901),
        (1900, 2000),
        (1900, 2500),
        (1950, 2050),
        (1950, 1950),
        (1975, 2089),
        (3978, 4789),
        (1900, 5123)
    ]))
    return ret

def find_solution_file(dir: Path, name: str) -> Tuple[Language, Path]:
    import glob 
    matched_files = glob.glob(f"{dir/name}.*")
    if not matched_files:
        raise FileNotFoundError(f"No matching files found for {name} in {dir}")
    if len(matched_files) > 1:
        raise FileNotFoundError(f"Found more than one matching file for {name} in {dir}")
    matched_file = Path(matched_files[0])
    ext = matched_file.suffix
    if ext == ".py":
        lang = Language.Python 
    elif ext in [".cc", ".cpp"]:
        lang = Language.Cpp
    else:
        raise FileNotFoundError(f"Found solution {matched_file} for {name} with unsupported language extension")
    return (lang, matched_file)

def check_results(dir: Path, problem: ProblemStatement) -> TestResult:
    lang, orig_input_file = find_solution_file(dir, problem.name)
    from tempfile import TemporaryDirectory
    import solutions
    with TemporaryDirectory() as tmpdir:
        import shutil
        dest_name = Path(tmpdir) / orig_input_file.name
        shutil.copyfile(orig_input_file, dest_name)
        executor = make_executor(lang, dest_name)
        import timeit
        start_time = timeit.default_timer()
        elapsed_time = 0.
        for input in problem.test_inputs:
            control_res = solutions.__dict__[problem.name](*input)
            try:
                test_res = executor.execute(input)
            except Exception as e:
                return TestResult(err=str(e))
            if control_res != test_res:
                return TestResult(err=f"Failure on input {input}. Expected {control_res}, got {test_res}")
        elapsed_time = timeit.default_timer() - start_time
    file_size = orig_input_file.stat().st_size
    return TestResult(size=file_size, time=elapsed_time)


def main():
    import argparse 
    parser = argparse.ArgumentParser("harness", "Testing harness for codegolf, supply file to use as argument")
    parser.add_argument("answerdir", metavar="answerdir", type=str)

    args = parser.parse_args()
    results = {}
    for problem in problem_list():
        results[problem.name] = check_results(Path(args.answerdir), problem)
    tot_size = 0
    for name, result in results.items():
        print(f"{name}: {result}")
        tot_size += result.size
    print(f"Total Size: {tot_size}")
    return 0 

if __name__ == "__main__":
    sys.exit(main())
