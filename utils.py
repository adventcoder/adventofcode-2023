import re

def ints(text):
    return map(int, re.findall(r'[+-]?[0-9]+', text))

def table(text, types=None, sep=None):
    table = []
    for line in text.splitlines():
        if line.strip():
            vals = line.split(sep)
            if types is not None:
                vals = [type(val) for val, type in zip(vals, types)]
            table.append(vals)
    return table
