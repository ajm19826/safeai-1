import re

def tokenize(text):
    return re.findall(r"\d+|\w+|[\+\-\*/]", text.lower())

def is_math(tokens):
    return any(t in "+-*/" for t in tokens)
