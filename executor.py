from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple,Any,Optional,List
from data import Language
import sys 
import subprocess 
from subprocess import PIPE
from inspect import Signature 

class Config():
    def __init__(self, lang: Language, file="./executors.json"):
        import json
        with open(file, "r") as jf:
            self.parsed_data = json.load(jf)[lang.name]

    def get_binary(self) -> str:
        return self.parsed_data["binary"]
    def get_args(self) -> List[str]:
        return self.parsed_data["args"]

def get_config(lang: Language, glbl_map={}) -> Config:
    nm = lang.name
    if nm not in glbl_map:
        glbl_map[nm] = Config(lang)
    return glbl_map[nm]

class Executor(ABC):
    @abstractmethod 
    def __init__(self, filename: Path, signature: Signature):
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
    def __init__(self, filename: Path, signature: Signature):
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
    cmd_args = [str(exec.test_dir / exec.test_name)]
    is_list = isinstance(args[0], list)
    if is_list:
        cmd_args += [str(x) for x in args[0]]
    else:
        cmd_args += [str(x) for x in args]
    return_type = exec.signature.return_annotation
    if return_type == str:
        cmd_args += ['S']
    if is_list:
        cmd_args += ['I']
    run_result = subprocess.run(cmd_args, capture_output=True)
    if run_result.returncode != 0:
        raise Exception(f"Run Failed, stderr: {run_result.stderr}")
    return return_type(run_result.stdout.decode())

class CExecutor(Executor):
    def __init__(self, filename: Path, signature: Signature):
        self.test_dir = filename.parent 
        self.test_name = filename.stem
        self.signature = signature
        conf = get_config(Language.C)
        cmd = [conf.get_binary()] + conf.get_args()
        cmd += ["-o", self.test_dir / self.test_name, "test_runner.c", filename]
        run_result = subprocess.run(cmd, capture_output=True)
        if run_result.returncode != 0:
            raise Exception(f"Compilation Failed: {run_result.stderr.decode()}")
    
    def execute(self, args: Tuple):
        return execute_c_common(self, args)
    
class CppExecutor(Executor):
    def __init__(self, filename: Path, signature: Signature):
        import shutil
        self.signature = signature
        self.test_dir = filename.parent 
        shutil.copy(filename, self.test_dir / "test_function.inc")
        self.test_name = filename.stem
        conf = get_config(Language.Cpp)
        cmd = [conf.get_binary()] + conf.get_args()
        cmd += ["-o", self.test_dir / self.test_name, "test_runner.cc", "-I", self.test_dir]
        run_result = subprocess.run(cmd, capture_output=True)
        if run_result.returncode != 0:
            raise Exception(f"Compilation Failed: {run_result.stderr.decode()}")

    def execute(self, args: Tuple):
        return execute_c_common(self, args)

class JSExecutor(Executor):
    def __init__(self, filename: Path, signature: Signature):
        self.filename = filename
        self.signature = signature  
    
    def execute(self, args: Tuple):
        bin = get_config(Language.Javascript).get_binary()
        node_process = subprocess.Popen([bin, "-i"], stdin=PIPE, stdout=PIPE)
        node_process.stdin.write(open(self.filename, "rb").read())
        eval_str = f"\nconsole.log();ans({','.join(repr(a) for a in args)})\n"
        try:
            out, err = node_process.communicate(input=eval_str.encode(), timeout=5)
        except Exception as e:
            node_process.kill()
            raise e
        if err:
            raise Exception(f"Error when running: {err.decode()}")
        ret = out.decode().splitlines()[-2]
        if self.signature.return_annotation == str:
            return ret.replace("'","")
        try: 
            return int(ret)
        except Exception as e:
            raise Exception(f"Error when running: {out.decode()}")

class APLExecutor(Executor):
    def __init__(self, filename: Path, signature: Signature):
        self.filename = filename
        self.signature = signature
    
    def execute(self, args: Tuple):
        bin = get_config(Language.APL).get_binary()
        cmd = [bin, "--script", "-f", self.filename]
        apl_process = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE)
        ans_input = f"{repr(args[1]) if len(args) > 1 else ''} ans {repr(args[0])}\n)OFF\n"
        try:
            out, err = apl_process.communicate(input=ans_input.encode(), timeout=5)
        except Exception as e:
            apl_process.kill()
            raise e 
        if err:
            raise Exception(f"Run Failed, stderr: {err.decode()}")
        return_type = self.signature.return_annotation
        return return_type(out.decode().replace(' ',''))

class PerlExecutor(Executor):
    def __init__(self, filename: Path, signature: Signature):
        self.filename = filename
        self.signature = signature

    def execute(self, args: Tuple):
        bin = get_config(Language.Perl).get_binary()
        cmd = [bin, self.filename]
        perl_process = subprocess.Popen([bin], stdin=PIPE, stdout=PIPE)
        perl_process.stdin.write(open(self.filename, "rb").read())
        eval_str = f"\nprint ans({','.join(repr(a) for a in args)})\n"
        try:
            out, err = perl_process.communicate(input=eval_str.encode(), timeout=5)
        except Exception as e:
            perl_process.kill()
            raise e
        if err:
            raise Exception(f"Error when running: {err.decode()}")
        ret = out.decode()
        if self.signature.return_annotation == str:
            return ret.replace("'","")
        try: 
            return int(ret)
        except Exception as e:
            raise Exception(f"Error when running: {out.decode()}")
        
def make_executor(lang: Language, filename: Path, signature: Signature) -> Executor:
    cls : Optional[Executor] = None
    if lang == Language.Python:
        cls = PythonExecutor
    elif lang == Language.C:
        cls = CExecutor
    elif lang == Language.Cpp:
        cls = CppExecutor
    elif lang == Language.Javascript:
        cls = JSExecutor
    elif lang == Language.APL:
        cls = APLExecutor
    elif lang == Language.Perl:
        cls = PerlExecutor
    if cls is None:
        raise Exception(f"Unsupported Language {lang}")
    return cls(filename, signature)

