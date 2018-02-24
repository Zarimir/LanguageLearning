import unittest
from modules.validator import *


class TestResult(unittest.TestCase):
    def test_has(self):
        key = 'key'
        string = 'string'
        obj = {key: string}
        self.assertEquals(string, has(obj, key, str))
        with self.assertRaises(ValueError):
            has(obj, key, int)
        with self.assertRaises(ValueError):
            has(obj, string, str)

    def test_valid_username(self):
        valid = 'Aa4.-_'
        invalid_char = '\t\n,?!@#$%^&*(){}[]\\'
        invalid = [
            '',
            'as'
        ]
        self.assertIsNone(valid_username(valid))
        for arg in invalid:
            with self.assertRaises(ValueError):
                valid_username(arg)
        for char in invalid_char:
            with self.assertRaises(ValueError):
                valid_username(valid + char)

    def test_valid_password(self):
        valid = 'AOWIdj '*2
        invalid = ''
        self.assertIsNone(valid_password(valid))
        with self.assertRaises(ValueError):
            valid_password(invalid)
