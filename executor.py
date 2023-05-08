from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple,Any,Optional
from data import Language
import sys 
import subprocess 
from subprocess import PIPE

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


def execute_c_common(exec: Any, args: Tuple) -> int:
    """
    Currently, the C executor assumes that
    (1) The output is a C long (Python int)
    (2) Each input is a C int
    If we get more diverse types, we'll have to add some technology here
    """
    run_result = subprocess.run([str(exec.test_dir / exec.test_name)] + [str(x) for x in args], capture_output=True)
    if run_result.returncode != 0:
        raise Exception(f"Run Failed, stderr: {run_result.stderr}")
    return int(run_result.stdout)

class CExecutor(Executor):
    def __init__(self, filename: Path):
        self.test_dir = filename.parent 
        self.test_name = filename.stem
        run_result = subprocess.run(["clang", "--std=c17", "-fsanitize=memory", "-o", self.test_dir / self.test_name, "test_runner.c", filename], capture_output=True)
        if run_result.returncode != 0:
            raise Exception(f"Compilation Failed: {run_result.stderr.decode()}")
    
    def execute(self, args: Tuple):
        return execute_c_common(self, args)
    
class CppExecutor(Executor):
    def __init__(self, filename: Path):
        import shutil
        self.test_dir = filename.parent 
        shutil.copy(filename, self.test_dir / "test_function.inc")
        self.test_name = filename.stem
        run_result = subprocess.run(["clang++", "--std=c++20", "-fsanitize=memory", "-o", self.test_dir / self.test_name, "test_runner.cc", "-I", self.test_dir], capture_output=True)
        if run_result.returncode != 0:
            raise Exception(f"Compilation Failed: {run_result.stderr.decode()}")

    def execute(self, args: Tuple):
        return execute_c_common(self, args)

class JSExecutor(Executor):
    def __init__(self, filename: Path):
        self.filename = filename 
    
    def execute(self, args: Tuple):
        node_process = subprocess.Popen(["node", "-i"], stdin=PIPE, stdout=PIPE)
        node_process.stdin.write(open(self.filename, "rb").read())
        eval_str = f"\nconsole.log();ans({','.join(str(a) for a in args)})\n"
        try:
            out, err = node_process.communicate(input=eval_str.encode(), timeout=5)
        except Exception as e:
            node_process.kill()
            raise e
        if err:
            raise Exception(f"Error when running: {err.decode()}")
        # NB: determine if we should output an int or not
        return int(out.decode().splitlines()[-2])
        
def make_executor(lang: Language, filename: Path) -> Executor:

    cls : Optional[Executor] = None
    if lang == Language.Python:
        cls = PythonExecutor
    elif lang == Language.C:
        cls = CExecutor
    elif lang == Language.Cpp:
        cls = CppExecutor
    elif lang == Language.Javascript:
        cls = JSExecutor
    if cls is None:
        raise Exception(f"Unsupported Language {lang}")
    return cls(filename)

