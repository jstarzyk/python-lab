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
    return not a or b


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
    return expr[i:i + 1], i + 1


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

    i = 0
    for m in range(2 ** len(_variables)):
        bins = [int(d) for d in format(m, '0%db' % len(_variables))]
        values = [d == 1 for d in bins]
        _globals = {'_xor': _xor, '_imp': _imp, '_equ': _equ}
        if eval(_template, _globals, dict(zip(_variables, values))):
            min_terms.append(((m,), tuple(bins)))
            i += 1

    if i == 0:
        always_evaluates_to = False
    elif i == 2 ** len(_variables):
        always_evaluates_to = True
    else:
        always_evaluates_to = None

    return min_terms, always_evaluates_to


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

    return tuple(res)


def create_groups(min_terms):
    groups = dict()

    for mt in min_terms:
        # n = len(list(filter(lambda x: x is True, mt[1])))
        n = len(list(filter(lambda x: x == 1, mt[1])))
        groups.setdefault(n, set())
        groups[n].add(mt)

    # for l in groups:
    #     groups[l] = set(groups[l])

    return collections.OrderedDict(sorted(groups.items(), key=lambda i: i[0]))


def merge_two_groups(g1, g2):
    # g1 = [([2], [0,0,1,0]), ([8], [1,0,0,0])]
    result = set()

    for mt1 in g1:
        bits1 = mt1[1]
        for mt2 in g2:
            bits2 = mt2[1]
            bits = diff_by_one(bits1, bits2)
            if bits:
                result.add((tuple(sorted(mt1[0] + mt2[0])), bits))

    return result


def merge_groups(groups):
    result = collections.OrderedDict()

    keys = list(groups)

    for i in range(len(keys) - 1):
        # result.append(merge_groups(groups[i], groups[i + 1]))
        res = merge_two_groups(groups[keys[i]], groups[keys[i + 1]])
        if res:
            result[keys[i]] = res

    return result


# def reduce_table():


def create_prime_implicant_table(groups, sv_min_terms):
    merged_min_terms = []
    for group in groups.values():
        for min_term in group:
            merged_min_terms.append(min_term)

    # pi_table = []
    pi_table = collections.OrderedDict()

    for sv_min_term in sv_min_terms:
        covers_min_term = []
        sv_min_term_val = sv_min_term[0][0]
        covers_n = 0
        for min_term in merged_min_terms:
            if sv_min_term_val in min_term[0]:
                covers_min_term.append(1)
                covers_n += 1
            else:
                covers_min_term.append(None)
        # pi_table.append([sv_min_term_val, covers_min_term])
        pi_table.setdefault(sv_min_term_val, [])
        pi_table[sv_min_term_val] = covers_min_term

    return pi_table, merged_min_terms


def covered_by_one(min_term):
    i = 0
    r = -1
    for c in range(len(min_term)):
        if min_term[c] == 1:
            r = c
            i += 1
        if i > 1:
            return -1
    return r


def get_prime_implicants(groups, min_terms):
    out = []

    table, merged_min_terms = create_prime_implicant_table(groups, min_terms)
    while len(table) > 0:
        pi = None
        app = None

        for t in table.items():
            pi = covered_by_one(t[1])
            if pi != -1:
                app = merged_min_terms.pop(pi)
                out.append(app)
                break

        if pi is None or app is None:
            return out

        del_mt = app[0]
        for mt in del_mt:
            if mt in table.keys():
                table.pop(mt)

        for t in table.items():
            t[1].pop(pi)

    return out


def make_expr(prime_implicants, variables):
    or_joined = []
    for p in prime_implicants:
        and_joined = []
        bits = p[1]
        for i in range(len(bits)):
            if bits[i] is None:
                continue
            elif bits[i] == 0:
                and_joined.append('~' + variables[i])
            elif bits[i] == 1:
                and_joined.append(variables[i])
        # or_joined.append('(' + ' & '.join(and_joined) + ')')
        or_joined.append(' & '.join(and_joined))

    return ' | '.join(or_joined)


def simplify(expr, mt, vr):
    if expr:
        template, variables = validate(expr)

        if template is None or variables is None:
            # print('%s is not a valid logical expression' % expr)
            return None

        min_terms, always_evaluates_to = get_min_terms(template, variables)

        if always_evaluates_to is not None:
            return always_evaluates_to
    else:
        min_terms = mt
        variables = vr

    groups = create_groups(min_terms)
    while True:
        res = merge_groups(groups)
        if res == collections.OrderedDict():
            break
        else:
            groups = res

    prime_implicants = get_prime_implicants(groups, min_terms)

    return make_expr(prime_implicants, variables)


def main():
    # examples = []
    # examples.append('1 | 0')
    # examples.append('a | b')
    # examples.append('b | ~b')
    print(simplify('a & ~a', None, None))


if __name__ == '__main__':
    main()
    # mm = [2, 6, 8, 9, 10, 11, 14, 15]
    # min_terms = sorted((((m,), tuple([int(d) for d in format(m, '0%db' % 4)])) for m in mm), key=lambda x: x[0][0])
    # print(simplify(None, min_terms, ['W', 'X', 'Y', 'Z']))

