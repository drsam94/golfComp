#!/usr/bin/python3
# Python 3.9.2

import sys
from pathlib import Path 
from typing import List, Any, Tuple, Iterable, Generator
from enum import Enum
from executor import make_executor
from data import Language, ProblemStatement, TestResult

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
        (1900, 5123),
        (1900, 9999),
        (1900, 1900)
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
    lang = Language.from_ext(ext)
    if not lang:
        raise FileNotFoundError(f"Found solution {matched_file} for {name} with unsupported language extension")
    return (lang, matched_file)

def check_results(dir: Path, problem: ProblemStatement) -> TestResult:
    try:
        lang, orig_input_file = find_solution_file(dir, problem.name)
    except Exception as e:
        return TestResult(err=str(e))
    from tempfile import TemporaryDirectory
    import solutions
    with TemporaryDirectory() as tmpdir:
        import shutil
        dest_name = Path(tmpdir) / orig_input_file.name
        shutil.copyfile(orig_input_file, dest_name)
        try:
            executor = make_executor(lang, dest_name)
        except Exception as e:
            return TestResult(err=str(e))
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
