#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 utils_test.py

# test partially
# python3 utils_test.py UtilsTestCase.test_to_str_bytes


from unittest import TestCase, main


# ------------------------------------------------------------------------------
# test
# ------------------------------------------------------------------------------

from utils import to_str

class UtilsTestCase(TestCase):

    # each function is single test
    def test_to_str_bytes(self):
        self.assertEqual('hello', to_str(b'hello'))

    def test_to_str_str(self):
        self.assertEqual('hello', to_str('hello'))

    def test_failing(self):
        self.assertEqual('incorrect', to_str('hello'))


if __name__ == '__main__':
    main()
