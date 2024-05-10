#!/usr/bin/env PYTHONHASHSEED=1234 python3

# db_connection.py
import __main__

class TestingDatabase:
    pass

class RealDatabase:
    pass

if __main__.TESTING:
    Database = TestingDatabase
else:
    Database = RealDatabase
