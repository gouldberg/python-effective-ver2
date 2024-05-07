#!/usr/bin/env PYTHONHASHSEED=1234 python3

# python3 integration_test.py

from unittest import TestCase, main


# ------------------------------------------------------------------------------
# set test harness (environment) for module level
# ------------------------------------------------------------------------------

# setUpModule is executed once, which is before setUp
def setUpModule():
    print('* Module setup')


# tearDownUpModule is executed once, which is after tearDown
def tearDownModule():
    print('* Module clean-up')


class IntegrationTest(TestCase):
    def setUp(self):
        print('* Test setup')

    def tearDown(self):
        print('* Test clean-up')

    def test_end_to_end1(self):
        print('* Test 1')

    def test_end_to_end2(self):
        print('* Test 2')


if __name__ == '__main__':
    main()
