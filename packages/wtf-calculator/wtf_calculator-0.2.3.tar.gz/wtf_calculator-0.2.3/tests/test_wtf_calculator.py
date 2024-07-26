# tests/test_wtf_calculator.py

import unittest
from wtf_calculator import absurd_add, absurd_subtract, absurd_multiply, absurd_divide, absurd_power, absurd_random, absurd_mod, absurd_cos, absurd_log, absurd_sin, absurd_sqrt

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

    def test_absurd_divid_by_zero(self):
        result = absurd_divide(1, 0)
        self.assertIsInstance(result, (str))

    def test_absurd_power(self):
        result = absurd_power(1, 1)
        self.assertIsInstance(result, (int, float))

    def test_absurd_sqrt(self):
        result = absurd_sqrt(1)
        self.assertIsInstance(result, (int, float))
    
    def test_absurd_log(self):
        result = absurd_log(1)
        self.assertIsInstance(result, (int, float))

    def test_absurd_log_a_negative(self):
        result = absurd_log(-1)
        self.assertIsInstance(result, (str))

    def test_absurd_log_a_zero(self):
        result = absurd_log(0)
        self.assertIsInstance(result, (str))

    def test_absurd_mod(self):
        result = absurd_mod(1, 1)
        self.assertIsInstance(result, (int, float))

    def test_absurd_mod_b_zero(self):
        result = absurd_mod(1, 0)
        self.assertIsInstance(result, (str))

    def test_absurd_sin(self):
        result = absurd_sin(1)
        self.assertIsInstance(result, (int, float))
    
    def test_absurd_cos(self):
        result = absurd_cos(1)
        self.assertIsIstance(result, (int, float))

    def test_absurd_random(self):
        result = absurd_random()
        self.assertisInstance(result, (int))


if __name__ == '__main__':
    unittest.main()
