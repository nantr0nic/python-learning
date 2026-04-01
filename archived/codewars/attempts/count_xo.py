"""
Check to see if a string has the same amount of 'x's and 'o's. 
The method must return a boolean and be case insensitive. 
The string can contain any char.
"""

def xo(s):
    x = 0
    o = 0
    for char in s:
        if char.lower() == 'x':
            x += 1
        if char.lower() == 'o':
            o += 1
    if x == o:
        return True
    else:
        return False

"""
Best solution:
def xo(s):
    s = s.lower()
    return s.count('x') == s.count('o')
"""

# REMEMBER ABOUT COUNT()!!!