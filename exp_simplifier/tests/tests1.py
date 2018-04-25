import unittest
import collections
from exp_simplifier.validate import *


# import re


class TestValidity(unittest.TestCase):
    def test_validate(self):
        # self.assertEqual(validate('(a | b) & c'), 1)
        self.assertTupleEqual(validate('(a | b) & c'), ('(a or b) and c', ['a', 'b', 'c']))
        self.assertTupleEqual(validate('~a|1&b^(~c)'), ('not a or True and b | _xor | (not c)', ['a', 'b', 'c']))
        # self.assertEqual(validate('(aaa | b) & c'), 1)
        # self.assertEqual(validate('a | b & c'), 1)
        # self.assertEqual(validate('a | b) & c'), 0)
        # self.assertEqual(validate('a | 1 & 0'), 1)
        # self.assertEqual(validate('a | 1 & >'), 0)
        # self.assertEqual(validate('~a | 1 & b ^ ~c'), 1)
        # self.assertEqual(validate('~a | 1 & b ^ (~c)'), 1)
        # self.assertEqual(validate('~a|1&b^(~c)'), 1)

    def test_get_min_terms(self):
        expr = '(a | b) & c'
        template, variables = validate(expr)
        self.assertEqual(get_min_terms(template, variables), ([((3,), (0, 1, 1)),
                                                              ((5,), (1, 0, 1)),
                                                              ((7,), (1, 1, 1))], None))

    def test_diff_by_one(self):
        self.assertEqual(diff_by_one((1, 0, None), (1, 0, None)), (1, 0, None))
        self.assertEqual(diff_by_one((1, 0, None), (1, 1, None)), (1, None, None))
        self.assertEqual(diff_by_one((0, 0, None), (1, 1, None)), None)
        self.assertEqual(diff_by_one((1, 0, None), (None, 0, None)), None)

    # def test_create_groups(self):
    #     self.assertEqual()

    def test_merge_two_groups(self):
        g1 = [((2,), (0, 0, 1, 0)), ((8,), (1, 0, 0, 0))]
        g2 = [((6,), (0, 1, 1, 0)), ((9,), (1, 0, 0, 1)), ((10,), (1, 0, 1, 0))]
        self.assertEqual(merge_two_groups(g1, g2), {((2, 6), (0, None, 1, 0)),
                                                    ((2, 10), (None, 0, 1, 0)),
                                                    ((8, 9), (1, 0, 0, None)),
                                                    ((8, 10), (1, 0, None, 0))})

    def test_create_groups(self):
        self.assertEqual(collections.OrderedDict({2: {((3,), (0, 1, 1)), ((5,), (1, 0, 1))},
                                                  3: {((7,), (1, 1, 1))}}),
                         create_groups([((3,), (0, 1, 1)),
                                        ((5,), (1, 0, 1)),
                                        ((7,), (1, 1, 1))]))

    def test_concat_groups(self):
        mm = [2, 6, 8, 9, 10, 11, 14, 15]
        min_terms = sorted((((m,), tuple([int(d) for d in format(m, '0%db' % 4)])) for m in mm), key=lambda x: x[0][0])
        groups = create_groups(min_terms)
        ccat = merge_groups(merge_groups(groups))
        d = collections.OrderedDict()
        d[1] = {((2, 6, 10, 14), (None, None, 1, 0)),
                ((8, 9, 10, 11), (1, 0, None, None))}
        d[2] = {((10, 11, 14, 15), (1, None, 1, None))}
        #
        self.assertEqual(ccat, d)

    def test_covered_by_one(self):
        self.assertEqual(covered_by_one([1, 1, None]), -1)
        self.assertEqual(covered_by_one([1, None, None]), 0)
        self.assertEqual(covered_by_one([None, None, None]), -1)
        self.assertEqual(covered_by_one([None, None, 1]), 2)

    def test_simplify(self):
        self.assertEqual(simplify('a | b', None, None), 'b | a')
        self.assertEqual(simplify('(a | b) & ~b', None, None), 'a & ~b')
        self.assertEqual(simplify('a | ~a', None, None), True)
        self.assertEqual(simplify('a | a', None, None), 'a')
        self.assertEqual(simplify('a & ~a', None, None), False)
        self.assertEqual(simplify('1', None, None), True)
        self.assertEqual(simplify('0 | 1', None, None), True)
        self.assertEqual(simplify('a > b', None, None), '~a | b')
        # self.assertEqual(simplify('a | ~a', None, None), 'True')

    # def test_tmp(self):
    #     self.assertEqual(re.findall('(\d\w)+', '~a|1&b\^(~c)'), ('a', 1, 'b', 'c'))


if __name__ == '__main__':
    unittest.main()
    # unittest.
    # mm = [2, 6, 8, 9, 10, 11, 14, 15]
    # min_terms = sorted((((m,), tuple([int(d) for d in format(m, '0%db' % 4)])) for m in mm), key=lambda x: x[0][0])
    # print(min_terms)
