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
### Javascript
extension .js
Node version 18.16.0
Define a function ans, arguments will be passed in the analagous types to python
### C++
extension: .cc
All C++ solutions must be compatible with clang 11.0.1-2 with `--std=c++20` and other flags, and should define a function like:
```
long ans(int x, int y) {

}
```
with the appropriate number of arguments. C++ will use `std::string` as the input and output type when strings are necessary.
You can write your code assuming `<string>` as well as a using statment `using std::string;` will be available. Similarly `vector<int>` will be used for
numeric list arguments. Note that, while it may be tempting to save characters, declarations like. `int x;`
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
APL is an interesting programming language for sure for golf. GNU APL 1.8 is supported.
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
### List
The central part of internal API.

    This represents a generic version of type 'origin' with type arguments 'params'.
    There are two kind of these aliases: user defined and special. The special ones
    are wrappers around builtin collections and ABCs in collections.abc. These must
    have 'name' always set. If 'inst' is False, then the alias can't be instantiated,
    this is used by e.g. typing.List and typing.Dict.
    
Function signature:
```
List(*args, **kwargs)
```
### test1

Find the sum of all positive integers less than the positive integer input k
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
those two years? (inclusive).
Use of an existing library like python datetime.date or a similar library that encodes
gregorian calendar rules is prohibited on this question
    
Function signature:
```
test2(start: int, end: int) -> int
```
### test3

The Look and Say sequence begins with a starting integer, and evolves via the rule that the next number
is constructed by replacing runs of numbers with their count, as though saying out their name, for example,
if the `start` value is 1:
1 -> "one one" -> 11 -> "two ones" -> 21 -> "one two, one one" -> 1211 -> "one one, one two, two ones" -> 111221
Given a `start` value, print out the value acheived after `count` iterations of this process
For example test3(1, 1) = 11 and test3(1, 2) = 21
Conditions:
 * `start` nor any member of a sequence from a provided start will contain the digit `0`
 * `count` >= 1
 * The result string will be at most 80 characters long
    
Function signature:
```
test3(start: str, count: int) -> str
```
### test4

Befunge is a 2-D Programming language with intentional bespoke semantics. For this problem, we will implement a
subset of Befunge, and your goal is to take as input a path to a file containing a befunge-subset program, and return
its integral output. The language operates with a single program stack, and starts evaluating left-to-right starting
with the first character in the file, though if special characters are hit, control flow will go in other directions.
If control flow would ever fall off the "edge" of the program, it wraps to the other side (top to bottom, left to right, etc)
If you would pop from an empty stack, the value 0 is used
See https://esolangs.org/wiki/Befunge for full details, but you must only implement the following operations (we removed most
operations related to IO or randomeness)
```
+   Addition: Pop two values a and b, then push the result of a+b
-   Subtraction: Pop two values a and b, then push the result of b-a
*   Multiplication: Pop two values a and b, then push the result of a*b
/   Integer division: Pop two values a and b, then push the result of b/a, rounded down. Undefined if a = 0.
%   Modulo: Pop two values a and b, then push the remainder of the integer division of b/a.
!   Logical NOT: Pop a value. If the value is zero, push 1; otherwise, push zero.
`   Greater than: Pop two values a and b, then push 1 if b>a, otherwise zero.
>   set direction right
<   set direction left
^   set direction up
v   set direction down
_   Horizontal IF: pop a value; set direction to right if value=0, set to left otherwise
|   Vertical IF: pop a value; set direction to down if value=0, set to up otherwise
:   Duplicate top stack value
\  Swap top stack values
$   pop tock stack value and discard
@   End program execution, returning the top of the stack as program output (0 if stack is empty)
```
Program size is at most 80 chars wide by 25 lines long.
All test input programs should terminate

Function signature:
```
test4(filename: str) -> int
```
### test5

    The game of Connect 4 is played on a board with 7 columns and 6 rows. Players alternate
    placing game pieces in one of the columns, where it will settle on top of any other pieces in
    that column. A player wins when any four of their pieces are in a line vertically, horizontally, or
    diagonally. Red always goes first.
    Your input is a list of plays in a Connect Four game, so for example the array
    `0,1,0,2,0,3,0`
    Would represent a game in which Red always plays in the leftmost column, while Black
    plays in other columns, and ends on Red's 4th turn.
    Your function should return the result of the game, meaning:
    `+N` if Red wins on their Nth turn
    `-N` if Black wins on their Nth turn
    0 if the game is a tie or is invalid
    A game is invalid if a player would attempt to place a seventh piece in one column.
    The input will be an array of integers in [0,6] inclusive.
    C signature:
    ```
    long test5(int* start, int* end)
    ```
    
Function signature:
```
test5(plays: List[int]) -> int
```

