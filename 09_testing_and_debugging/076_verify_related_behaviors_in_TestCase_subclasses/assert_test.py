#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 assert_test.py

from unittest import TestCase, main


# ------------------------------------------------------------------------------
# TestCase provides helper function for assertion, such as assertEqual and assertTrue.
# Those are more helpful than built-in assert expression,
# since those helpers output input/output and make failures understandable
# ------------------------------------------------------------------------------

from utils import to_str

class AssertTestCase(TestCase):
    def test_assert_helper(self):
        expected = 12
        found = 2 * 5
        self.assertEqual(expected, found)

    def test_assert_statement(self):
        expected = 12
        found = 2 * 5
        assert expected == found


if __name__ == '__main__':
    main()
