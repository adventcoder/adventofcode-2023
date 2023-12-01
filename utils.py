import re

def ints(text):
    return map(int, re.findall(r'[+-]?[0-9]+', text))
