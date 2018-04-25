import string
import collections
import re
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
def _xor(a, b):
    return (a and not b) or (not a and b)


@Infix
def _imp(a, b):
    return not a and b


@Infix
def _equ(a, b):
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


def consume_variable(expr, i):
    for j in range(i + 1, i + len(expr[i:])):
        if not expr[j].isalpha():
            return expr[i:j], j
    return expr[i:i+1], i + 1


def validate(expr):
    state = State.S1
    parens = 0
    template = ''
    variables = set()

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
                var, i = consume_variable(expr, i)
                if is_variable(var):
                    state = State.S2
                    if var == '1':
                        var = 'True'
                    elif var == '0':
                        var = 'False'
                    else:
                        variables.add(var)
                    template += var
                else:
                    return None, None
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
                        inf = ' | _xor | '
                    elif op == '~':
                        inf = 'not '
                    elif op == '>':
                        inf = ' | _imp | '
                    elif op == '=':
                        inf = ' | _equ | '

                    template += inf
                    state = State.S1
                    i += 1
                else:
                    return None, None
        if parens < 0:
            return None, None
    if parens == 0 and state == State.S2:
        return re.sub(' {2,}', ' ', template), sorted(variables)
    else:
        return None, None


def get_min_terms(_template, _variables):
    min_terms = []

    for m in range(2 ** len(_variables)):
        bins = [int(d) for d in format(m, '0%db' % len(_variables))]
        values = [d == 1 for d in bins]
        _globals = {'_xor': _xor, '_imp': _imp, '_equ': _equ}
        if eval(_template, _globals, dict(zip(_variables, values))):
            min_terms.append(([m], bins))

    return min_terms


def diff_by_one(bits1, bits2):
    len_bits = len(bits1)
    diffs = 0
    res = []

    for i in range(len_bits):
        if (bits1[i] is None) | _xor | (bits2[i] is None):
            return None
        else:
            if bits1[i] != bits2[i]:
                diffs += 1
                res.append(None)
            else:
                res.append(bits1[i])
            if diffs > 1:
                return None

    return res


def create_groups(min_terms):
    groups = {}

    for mt in min_terms:
        # n = len(list(filter(lambda x: x is True, mt[1])))
        n = len(list(filter(lambda x: x == 1, mt[1])))
        groups.setdefault(n, [])
        groups[n].append(mt)

    return collections.OrderedDict(sorted(groups.items(), key=lambda i: i[0]))


def merge_groups(g1, g2):
    # g1 = [([2], [0,0,1,0]), ([8], [1,0,0,0])]
    result = []

    for mt1 in g1:
        bits1 = mt1[1]
        for mt2 in g2:
            bits2 = mt2[1]
            bits = diff_by_one(bits1, bits2)
            if bits:
                result.append((sorted(mt1[0] + mt2[0]), bits))

    return result


def concat_groups(groups):
    result = collections.OrderedDict()

    keys = list(groups)

    for i in range(len(keys) - 1):
        # result.append(merge_groups(groups[i], groups[i + 1]))
        res = merge_groups(groups[keys[i]], groups[keys[i + 1]])
        if res:
            result[keys[i]] = res

    return result


# if __name__ == '__main__':
#     # e1 = '(a | b)'
#     # e1 = '(aaa | b) & c'
#     # e2 = 'a | 1b & 0'
#     # e2 = ')a | 1b & 0'
#     e3 = '~x|1&b^(~c)'
#     # print(validate(e1))
#     # print(validate(e2))
#     # print(validate(e3))
#     _template, variables = validate(e3)
#     variables = sorted(variables)
#     print(_template, variables)
#     print(get_min_terms(_template, variables))
