import unittest
from exp_simplifier.validate import validate
# import re


class TestValidity(unittest.TestCase):
    def test_validity(self):
        self.assertEqual(validate('(a | b) & c'), True)
        self.assertEqual(validate('(aaa | b) & c'), True)
        self.assertEqual(validate('a | b & c'), True)
        self.assertEqual(validate('a | b) & c'), False)
        self.assertEqual(validate('a | 1 & 0'), True)
        self.assertEqual(validate('a | 1 & >'), False)
        self.assertEqual(validate('~a | 1 & b ^ ~c'), True)
        self.assertEqual(validate('~a | 1 & b ^ (~c)'), True)
        self.assertEqual(validate('~a|1&b^(~c)'), True)

    # def test_tmp(self):
    #     self.assertEqual(re.findall('[\d\w]+', '~a|1&b\^(~c)'), ['a', '1', 'b', 'c'])


if __name__ == '__main__':
    unittest.main()
