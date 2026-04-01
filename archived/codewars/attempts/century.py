def century(year):
    if len(str(year)) == 2:
        return 1
    elif len(str(year)) == 3:
        first_digit = list(str(year))[0]
        return int(first_digit) + 1
    elif len(str(year)) >= 4:
        pass
        # This is a bad solution.
    return

"""
Best solution:

def century(year):
    return (year + 99) // 100

"""

# Use ceiling division and basic arithmetic.