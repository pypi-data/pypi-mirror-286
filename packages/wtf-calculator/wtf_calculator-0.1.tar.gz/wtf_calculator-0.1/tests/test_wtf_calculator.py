# tests/test_wtf_calculator.py

import unittest
from wtf_calculator import absurd_add, absurd_subtract, absurd_multiply, absurd_divide

class TestWtfCalculator(unittest.TestCase):

    def test_absurd_add(self):
        result = absurd_add(1, 1)
        self.assertIsInstance(result, int)

    def test_absurd_subtract(self):
        result = absurd_subtract(1, 1)
        self.assertIsInstance(result, int)

    def test_absurd_multiply(self):
        result = absurd_multiply(1, 1)
        self.assertIsInstance(result, int)

    def test_absurd_divide(self):
        result = absurd_divide(1, 1)
        self.assertIsInstance(result, (int, float))
        self.assertNotEqual(result, float('inf'))

if __name__ == '__main__':
    unittest.main()
