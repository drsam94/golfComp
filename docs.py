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
All C++ solutions must be compatible with clang 11.0.1-2 with `--std=c++20` and other flags, and should define a function like: 
```
long ans(int x, int y) {

}
```
with the appropriate number of arguments. C++ will use `std::string` as the input and output type when strings are necessary. 
You can write your code assuming `<string>` as well as a using statment `using std::string;` are available
Note that, while it may be tempting to save characters, declarations like. `int x;` 
will declare an uninitialized variable on the stack. While you may be able to run it locally in such a way that such code passes,
the testing harness will attempt to make your code fail if you try such tricks. Locally running with `fsanitize=memory` can catch many,
but not all issues of this form. Other kinds of UB are "okay" if you can get away with it as the code does only have to work for one set of 
compiler flags, but reading uninitialized memory effectively adds an implicit dependence for your code on the calling code, which you do not have access to.
### C
extension: .c
All C solutions must be compilable with clang 11.0.1-2 with `--std=c17` and other flags, and should define a function that will be called through the
declaration
```
extern long ans();
```
It will be called with a series of arguments agreeing with the python signature: `char*` for `str`, `int` for `int`, and with a final 
`char*` outparam if the function returns a string in python. You can safely assume that outparam has enough memory allocated to write 
the solution. See the following examples:
```
// Python signature (int, int) -> int
long ans(int x, int y) { ... }
// Python signature (str, int) -> str
void ans(char* x, int y, char* out) { ... }
```
All the notes in the `C++` section about UB apply here as well
### APL
APL is an interesting programming language for sure for golf. APL 1.8 is supported.
The arguments to the program will be passed, as integer numbers or character arrays, to your function defined `ans`, such as with
```
∇Y ← ans x
Y ← 2 + x
∇
```
You should have a script with just the function definition.
All problems will have 1 or 2 arguments, so define a unary or binary operator -- in the case of binary, the argument that
is usually considered "second" in other languages will be the left-hand operand.
Do not end your script with `)OFF` as your function will be called before closing the script. Solutions in APL, like all other languages, will be graded on number of *characters*, not number of bytes
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