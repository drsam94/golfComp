
def test1(k: int) -> int:
    """
    Find the sum of all positive integers less than the input k
    which are a multiple of 3 or a multiple of 5.
    For example, the list of numbers satisfying this property that 
    are less than 10 is 3,5,6,9 so therefore the answer is their sum, 23
    """
    return sum(x for x in range(k) if x % 3 == 0 or x % 5 == 0)

def test2(s: int, e: int) -> int:
    """
    1 Jan 1900 was a Monday
    A leap year occurs on most years divisible by 4, but if the year is divisble by 
    100 and not 400, it is not a leap year
    30 days hath September, April, June and November

    Given a start year >= 1900 and and an end year, how many "Friday the 13ths" occurred between
    those two years (inclusive)
    """ 
    month_size = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ret = 0
    day_of_week = 0
    friday = 4
    day_of_month = 0
    month = 0
    year = 1900
    while year <= e:
        if day_of_week == friday and day_of_month == 12 and year >= s:
            ret += 1
        day_of_week += 1 
        day_of_week %= 7
        day_of_month += 1
        eom = month_size[month]
        if month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            eom += 1
        if day_of_month == eom:
            day_of_month = 0
            month += 1
        if month == 12:
            month = 0
            year += 1
    return ret    
