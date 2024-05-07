#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 utils_error_test.py

# test partially
# python3 utils_error_test.py UtilsErrorTestCase.test_to_str_bad


from unittest import TestCase, main


# ------------------------------------------------------------------------------
# with assertRaises
# for exception raising
# ------------------------------------------------------------------------------

from utils import to_str

class UtilsErrorTestCase(TestCase):
    def test_to_str_bad(self):
        with self.assertRaises(TypeError):
            to_str(object())

    def test_to_str_bad_encoding(self):
        with self.assertRaises(UnicodeDecodeError):
            to_str(b'\xfa\xfa')


if __name__ == '__main__':
    main()
