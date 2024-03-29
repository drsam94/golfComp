#!/usr/bin/python3
# Python 3.9.2

import sys
from pathlib import Path 
from typing import List, Any, Tuple, Iterable, Dict
from executor import make_executor
from data import Language, ProblemStatement, TestResult
import inspect 

def wrap_in_tuple(input: Iterable[Any]) -> Iterable[Any]:
    for elem in input:
        yield (elem,)

def problem_list() -> List[ProblemStatement]:
    ret = []
    ret.append(ProblemStatement("test1", wrap_in_tuple(list(range(1,10)) + [25, 45, 1000, 10000, 99999])))
    ret.append(ProblemStatement("test2", [
        (1900, 1901),
        (1900, 1902),
        (1900, 1903),
        (1900, 1905),
        (1900, 2000),
        (1900, 2500),
        (1901, 1902),
        (1950, 2050),
        (1950, 1950),
        (1975, 2089),
        (3978, 4789),
        # (1900, 5123),
        # (1900, 9999),
        (1900, 1900)
    ]))
    ret.append(ProblemStatement("test3", [
        ('1', 1),
        ('1', 8),
        ('1', 12),
        ('13', 13),
        ('99', 5),
        ('1234', 4),
        ('12345', 4)
    ]))
    ret.append(ProblemStatement("test4", wrap_in_tuple([
        "reference_files/befunge/factorial.fun",
        "reference_files/befunge/test_math.fun",
        "reference_files/befunge/maze.fun",
        "reference_files/befunge/sparse.fun"
    ])))
    ret.append(ProblemStatement("test5", wrap_in_tuple([
        [0,1,0,2,0,3,0],
        [0,1,1,2,2,1,2,3,3,3,3],
        [0,1,2,3,3,2,1,0,0,6,1,6,2,6,3,6],
        [0,1,2,3,4,5,6,0,1,2,3,4,5,6],
        [0,0,0,0,0,0,0,0,0,0,0,0],
        [6,6,6,6,6,6,6,6,6,6]
    ])))
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

def check_results(dir: Path, problem: ProblemStatement, print_answers: bool) -> TestResult:
    try:
        lang, orig_input_file = find_solution_file(dir, problem.name)
    except Exception as e:
        return TestResult(err=str(e))
    from tempfile import TemporaryDirectory
    import solutions
    soln = solutions.__dict__[problem.name]
    with TemporaryDirectory() as tmpdir:
        import shutil
        dest_name = Path(tmpdir) / orig_input_file.name
        shutil.copyfile(orig_input_file, dest_name)
        try:
            executor = make_executor(lang, dest_name, inspect.signature(soln))
        except Exception as e:
            return TestResult(err=str(e))
        import timeit
        start_time = timeit.default_timer()
        elapsed_time = 0.
        for input in problem.test_inputs:
            control_res = soln(*input)
            try:
                test_res = executor.execute(input)
            except Exception as e:
                return TestResult(err=str(e))
            if control_res != test_res:
                return TestResult(err=f"Failure on input {input}. Expected {control_res}, got {test_res}")
            if print_answers:
                print(f"{problem.name}: {input} = {control_res}")
        elapsed_time = timeit.default_timer() - start_time
    with open(orig_input_file, "r") as o_file:
        # This is the size in _characters_, not in bytes, intentionally!
        file_size = len(o_file.read())
    return TestResult(size=file_size, time=elapsed_time,lang=lang)

def save_results(results: Dict[str, TestResult]):
    import json
    if results and all(res.is_valid() for _,res in results.items()):
        lang = None
        for _,res in results.items():
            if lang is None:
                lang = res.lang
            elif lang != res.lang:
                lang = None
                break
        key = lang.name if lang else "Any"
        with open('results.json', 'r') as jf:
            res_json = json.load(jf)
        if key not in res_json:
            res_json[key] = {}
        user = 'samdonow'
        if user not in res_json[key]:
            res_json[key][user] = {}
        write_map = res_json[key][user]
        for name, res in results.items():
            write_map[name] = res.size
        with open('results.json', 'w') as jf:
            json.dump(res_json, jf)
    
def main():
    import argparse 
    parser = argparse.ArgumentParser("harness", "Testing harness for codegolf, supply file to use as argument")
    parser.add_argument("answerdir", metavar="answerdir", type=str)
    parser.add_argument("--printanswers", action="store_true")
    args = parser.parse_args()
    results = {}
    for problem in problem_list():
        results[problem.name] = check_results(Path(args.answerdir), problem, args.printanswers)
    tot_size = 0
    for name, result in results.items():
        print(f"{name}: {result}")
        tot_size += result.size
    print(f"Total Size: {tot_size}")
    save_results(results)
    return 0 

if __name__ == "__main__":
    sys.exit(main())
