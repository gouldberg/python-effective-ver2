#!/usr/bin/env PYTHONHASHSEED=1234 python3

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main


# ------------------------------------------------------------------------------
# set test harness (environment)
#   Override setUp and tearDown of TestCase subclass
# NOTE: this is applied defined tests only.
# ------------------------------------------------------------------------------

class EnvironmentTest(TestCase):
    
    # before test:  make directory for test
    def setUp(self):
        self.test_dir = TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

    # after test:  delete
    def tearDown(self):
        self.test_dir.cleanup()

    def test_modify_file(self):
        with open(self.test_path / 'data.bin', 'w') as f:
            f.write('hello')


if __name__ == '__main__':
    main()
