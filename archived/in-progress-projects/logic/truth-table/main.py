import re

from logic import Logic

p = True
q = True

op = Logic(p, q)

AND = "^"
OR = "V"
IF = ">"
NOT = "-"

input_string = input(" >> ")

patterns = r'(\S)([\^V\>-])(\S)'

matches = re.findall(patterns, input_string)
"""
print(matches)

for match in matches:
    print(f"Character before: {match[0]}, Target character: {match[1]}, Character after: {match[2]}")

if match[1] == AND:
    print(op.andF(p,q))
"""
print(op.ifF(op.orF(p,q), q))


