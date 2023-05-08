
def test1(k: int) -> int:
    """
    Find the sum of all positive integers less than the input k
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

def test3(multiplier: int, modulus: int) -> int:
    """
    For a given number N, consider the sequence of numbers s_n(N) forms by taking substrings from the left, e.g
    1234567890 -> [1, 12, 123, 1234, 12345, 123456, 1234567, 12345678, 123456789] = 
    We say that a sequence a_n divides a sequence s_n if for each 1 <= i <= n, a_i divides s_i 
    (note we start i at 1, skipping the first element)
    Now consider the sequence formed my a multiplier K and a modulus m, defined by `a_n = (n*K) mod m`
    
    Given the inputs of `multiplier` 1 <= K <= 100 and a `modulus` 2 <= m <= 100, find the sum of all 10-digit numbers N which:
     * Contain each of the digits 0-9 exactly once
     * a_n(K, m) divides s_n(N)
    """
