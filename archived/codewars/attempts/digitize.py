def digitize(n):
    string_list = list(str(n))
    reversed = []
    while string_list:
        reversed.append(int(string_list.pop()))
    return reversed

"""
Best solution found:
def digitize(n):
    return [int(x) for x in str(n)[::-1]]
"""