import string
from enum import Enum
from functools import partial


class Infix(object):

    def __init__(self, func):
        self.func = func

    def __or__(self, other):
        return self.func(other)

    def __ror__(self, other):
        return Infix(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)


@Infix
def xor(a, b):
    return (a and not b) or (not a and b)


@Infix
def imp(a, b):
    return not a and b


@Infix
def equ(a, b):
    return (a and b) or (not a and not b)


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


def validate(expr):
    state = State.S1
    parens = 0
    # variables = []
    template = ''
    len_template = 0
    elems = []
    indexes = {}

    i = 0
    while i < len(expr):
        s = expr[i]
        if s == ' ':
            template += s
            i += 1
            continue
        if state == State.S1:
            if s == '(':
                template += s
                parens += 1
                i += 1
            elif s == '~':
                template += 'not '
                i += 1
            else:
                var, i = consume(expr, i)
                if is_variable(var):
                    state = State.S2

                    if template != '':
                        elems.append(template)
                        template = ''
                        len_template += 1

                    elems.append(var)

                    if var in indexes:
                        indexes[var].append(len_template)
                    else:
                        indexes[var] = [len_template]

                    len_template += 1
                else:
                    return False, None, None
        elif state == State.S2:
            if s == ')':
                template += s
                parens -= 1
                i += 1
            else:
                # operators = '&|^~>='
                pos = operators.index(s)
                if pos != -1:
                    inf = ''
                    op = operators[pos]
                    if op == '&':
                        inf = ' and '
                    elif op == '|':
                        inf = ' or '
                    elif op == '^':
                        inf = ' |xor| '
                    elif op == '~':
                        inf = 'not '
                    elif op == '>':
                        inf = ' |imp| '
                    elif op == '=':
                        inf = ' |equ| '

                    template += inf
                    state = State.S1
                    i += 1
                else:
                    return False, None, None
        if parens < 0:
            return False, None, None

    if template != '':
        elems.append(template)
    return (parens == 0 and state == State.S2), elems, indexes


# if __name__ == '__main__':
#     e1 = '(aaa | b) & c'
#     e2 = 'a | 1 & 0'
#     e3 = '~a|1&b^(~c)'
#     print(validate(e1))
#     print(validate(e2))
#     print(validate(e3))
