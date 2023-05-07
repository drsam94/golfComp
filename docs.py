#!/usr/bin/python3
# Python 3.9.2
def intro():
    return """# 2023 Summer Code Golf Competition
The goal of Code Golf is to solve problems using as little code as possible. While there are potentially multiple
ways to define "as little code," in this challenge, it is defines as the number of characters in the source code
file which defines the function. The circumstances around the solution are restricted, which limits the use of
certain hacks. In all cases, the "challenge" will involve writing a function satisfying a certain contract which takes
the inputs and translates them to the outputs. All solutions must:
  * Be written in a supported programming language following the set standards for that language
  * Not depend on any files or other resources outside of the submitted solution file
  * Must run within a reasonable length of time (about a minute)
  * Be in a file named like `name.ext` where "name" is the name of the problem as defined below (case-sensitive) and ext is the canonical extension for the language
## Supported languages
The following languages are supported in this competition, if you wish to compete in a different language, 
you can help write an `Executor` class for the testing harness
### Python 3
extension: .py
All python solutions must be written in Python 3.9.2, with only standard libraries capable of being imported, and must
have their solution computed by a function named `ans` which satisfies the specified contract of inputs and output type. 
For example, if a problem was just to compute the sum of three integers, you could submit the following solution:
```
def ans(x, y, z):
    return x + y + z
```
Or, for a better codegolf solution:
```
ans=lambda*a:sum(a)
```
### C++
extension: .cc
I haven't specified this yet
## Problems
The following is the list of problems in the challenge
"""
def main():
    import solutions 
    import inspect
    output_doc = intro()
    functions = [f for f in solutions.__dict__.items() if callable(f[1])]
    for name, f in functions:
        sig = str(inspect.signature(f))
        section = f"### {name}\n{f.__doc__}\nFunction signature:\n```\n{name}{sig}\n```\n"
        output_doc += section
    print(output_doc)

if __name__ == "__main__":
    main()