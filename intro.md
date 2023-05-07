# 2023 Summer Code Golf Competition
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
All C++ solutions must be compatible with gcc 10.2.1 with `--std=c++20`, and should define a function like: 
```
long ans(int x, int y) {

}
```
with the appropriate number of arguments.
### C
extension: .c
All C solutions must be compilable with gcc 10.2.1 with `--std=c17`, and should define a function like:
```
long ans(int x, int y) {

}
```
with the appropriate number of arguments. Do note that you must simply define a function which can be called by passing
the appropriate number of arguments with the appropriate times: the actual definition can look different (e.g "implicit int")
## Problems
The following is the list of problems in the challenge
### test1

    Find the sum of all positive integers less than the input k
    which are a multiple of 3 or a multiple of 5.
    For example, the list of numbers satisfying this property that 
    are less than 10 is 3,5,6,9 so therefore the answer is their sum, 23
    
Function signature:
```
test1(k: int) -> int
```
### test2

    1 Jan 1900 was a Monday
    A leap year occurs on most years divisible by 4, but if the year is divisble by 
    100 and not 400, it is not a leap year
    30 days hath September, April, June and November

    Given 1900 <= start_year <= end_year <= 9999, how many "Friday the 13ths" occurred between
    those two years? (inclusive)
    
Function signature:
```
test2(start: int, end: int) -> int
```

