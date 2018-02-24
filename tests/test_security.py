import unittest
from modules.validator import *
from modules.security import *


class TestSecurity(unittest.TestCase):
    def setUp(self):
        self.string = "AOWifAWOfi jawofiaj fawf"

    def test_encode(self):
        encoded = encode(self.string)
        self.assertIs(bytes, type(encoded))
        second = encode(encoded)
        self.assertIs(bytes, type(second))
        self.assertEqual(second, encoded)

    def test_decode(self):
        decoded = decode(encode(self.string))
        self.assertIs(str, type(decoded))
        self.assertEquals(self.string, decoded)

        second = decode(decoded)
        self.assertIs(str, type(second))
        self.assertEquals(self.string, decoded)
        self.assertEquals(second, decoded)

    def test_hashpw(self):
        hashed = hashpw(self.string)
        self.assertIs(str, type(hashed))
        self.assertNotEqual(hashed, hashpw(self.string))

    def test_checkpw(self):
        hashed = hashpw(self.string)
        self.assertTrue(checkpw(self.string, hashed))
        self.assertFalse(checkpw(self.string + "aowif", hashed))