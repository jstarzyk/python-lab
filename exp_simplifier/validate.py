import string
from enum import Enum

# variables = string.ascii_lowercase
alphanumeric = string.ascii_letters + string.digits
operators = '&|^~>='


class State(Enum):
    S1 = 1
    S2 = 2


def is_variable(var):
    for s in var:
        if s not in alphanumeric:
            return False
    return True


def consume(expr, i):
    for j in range(i + 1, i + len(expr[i:])):
        if not expr[j].isalpha():
            return expr[i:j], j
    return expr[i:i+1], i + 1
    # res = expr[i:].split(' ', 1)
    # return res[0], i + len(res[0])


def validate(expr):
    state = State.S1
    parens = 0

    i = 0
    while i < len(expr):
        if expr[i] == ' ':
            i += 1
            continue
        if state == State.S1:
            if expr[i] == '(':
                parens += 1
                i += 1
            elif expr[i] == '~':
                i += 1
            else:
                var, i = consume(expr, i)
                if is_variable(var):
                    state = State.S2
                else:
                    return False
        elif state == State.S2:
            if expr[i] == ')':
                parens -= 1
                i += 1
            else:
                if expr[i] in operators:
                    state = State.S1
                    i += 1
                else:
                    return False
        if parens < 0:
            return False
    return parens == 0 and state == State.S2

