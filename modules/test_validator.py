import unittest
from modules.validator import *


class TestResult(unittest.TestCase):
    def test_has(self):
        key = 'key'
        string = 'string'
        obj = {key: string}
        self.assertTrue(has(obj, key, str))
        self.assertFalse(has(obj, key, int))
        self.assertFalse(has(obj, string, str))

    def test_valid_username(self):
        valid = 'Aa4.-_'
        invalid_char = '\t\n,?!@#$%^&*(){}[]\\'
        invalid = [
            '',
            'as'
        ]
        self.assertTrue(valid)
        for arg in invalid:
            self.assertFalse(valid_username(arg))
        for char in invalid_char:
            self.assertFalse(valid_username(valid + char))

    def test_valid_password(self):
        valid = 'AOWIdj '
        invalid = ''
        self.assertTrue(valid_password(valid))
        self.assertFalse(valid_password(invalid))
