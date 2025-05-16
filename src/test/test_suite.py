import os
import sys
import unittest

loader = unittest.TestLoader()
suite = loader.discover(start_dir=os.getcwd(), pattern="*_test.py")

runner = unittest.TextTestRunner()
result = runner.run(suite).wasSuccessful()

if not result:
    sys.exit("Some tests failed. Please check the output above for details.")
