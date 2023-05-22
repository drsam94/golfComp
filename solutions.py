from typing import List 

def test1(k: int) -> int:
    """
Find the sum of all positive integers less than the positive integer input k
which are a multiple of 3 or a multiple of 5.
For example, the list of numbers satisfying this property that 
are less than 10 is 3,5,6,9 so therefore the answer is their sum, 23
    """
    return sum(x for x in range(k) if x % 3 == 0 or x % 5 == 0)

def test2(start: int, end: int) -> int:
    """
1 Jan 1900 was a Monday
A leap year occurs on most years divisible by 4, but if the year is divisble by 
100 and not 400, it is not a leap year
30 days hath September, April, June and November

Given 1900 <= start_year <= end_year <= 9999, how many "Friday the 13ths" occurred between
those two years? (inclusive)
    """ 
    month_size = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ret = 0
    day_of_week = 0
    friday = 4
    day_of_month = 0
    month = 0
    year = 1900
    while year <= end:
        if day_of_week == friday and day_of_month == 12 and year >= start:
            ret += 1
        day_of_week += 1 
        day_of_week %= 7
        day_of_month += 1
        eom = month_size[month]
        if month == 1 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            eom += 1
        if day_of_month == eom:
            day_of_month = 0
            month += 1
        if month == 12:
            month = 0
            year += 1
    return ret    

def test3(start: str, count: int) -> str:
    """
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
    """
    val = start
    remaining = count 
    while remaining > 0:
        last = ''
        next_val = ''
        run_length = 0 
        for c in val:
            if run_length == 0:
                last = c 
                run_length += 1
            elif c == last:
                run_length += 1
            else:
                next_val += str(run_length)
                next_val += last 
                run_length = 1
                last = c 
        next_val += str(run_length)
        next_val += last 
        val = next_val
        remaining -= 1
    return val

def test4(filename: str) -> int:
    """
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
\\  Swap top stack values
$   pop tock stack value and discard
@   End program execution, returning the top of the stack as program output (0 if stack is empty)
```
Program size is at most 80 chars wide by 25 lines long.
All test input programs should terminate
"""
    program = open(filename).read().splitlines()
    stack: List[int] = []
    pop = lambda : stack.pop() if stack else 0
    pc = [0, 0]
    dir = [1, 0]
    while True:
        line = program[pc[1]]
        op = line[pc[0]] if pc[0] < len(line) else " "
        if op in '+-*/%`\\':
            a = pop()
            b = pop()
            if op == '\\':
                stack.append(a)
                stack.append(b)
            else:
                if op == '+':
                    v = a + b 
                elif op == '-':
                    v = b - a 
                elif op == '*':
                    v = b * a
                elif op == '%':
                    v = b % a 
                elif op == '/':
                    v = b // a 
                elif op == '`':
                    v = int(b > a)
                stack.append(v)
        
        if op == '<':
            dir = [-1, 0]
        elif op == '>':
            dir = [1, 0]
        elif op == '^':
            dir = [0, -1]
        elif op == 'v':
            dir = [0, 1]
        elif op in '0123456789':
            stack.append(int(op))
        elif op == '_':
            dir[1] = 0
            dir[0] = -1 if pop() else 1
        elif op == '|':
            dir[0] = 0
            dir[1] = -1 if pop() else 1 
        elif op == ':':
            x = pop()
            stack.append(x)
            stack.append(x)
        elif op == '$':
            pop()
        elif op == '!':
            stack.append(pop()==0)
        elif op == '@':
            return pop()
        if dir[0]:
            pc[0] = (pc[0] + dir[0]) % 80
        if dir[1]:
            pc[1] = (pc[1] + dir[1]) % len(program)
