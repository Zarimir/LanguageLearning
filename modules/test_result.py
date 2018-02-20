import unittest
import config
from modules.result import Result


class TestResult(unittest.TestCase):
    def setUp(self):
        self.result = Result()

    def test_bool(self):
        self.assertTrue(self.result)

        self.result = Result()
        self.result.value = False
        self.assertFalse(self.result)
        self.result.value = True
        self.assertTrue(self.result)

        self.assertFalse(Result(False))

    def test_consume(self):
        key = "key"
        value = "value"
        self.result.consume({key: value})
        print("lala")
        self.assertTrue(key in self.result)
        self.assertTrue(self.result[key] == value)

    def test_fail(self):
        self.result.fail({})
        self.assertFalse(self.result)

    def test_crash(self):
        self.result.crash()
        self.assertFalse(self.result)
        self.assertTrue(config.internal_error in self.result)
        self.assertTrue(self.result[config.internal_error])

    def test_succeed(self):
        result = Result(False)
        self.result.succeed()
        self.assertTrue(self.result)

    def test_update(self):
        key = "key"
        value = "value"
        result = Result()
        result.consume({key: value})

        self.result.update(result)
        self.assertTrue(result)
        self.assertTrue(key in self.result)
        self.assertTrue(self.result[key] == value)

        self.setUp()
        self.result.update(result, invert=True)
        self.assertFalse(result)
        self.assertTrue(key not in self.result)

        self.setUp()
        result.value = False
        self.result.update(result)
        self.assertFalse(result)
        self.assertTrue(key in self.result)
        self.assertTrue(self.result[key] == value)

        self.setUp()
        self.result.update(result, invert=True)
        self.assertTrue(result)
        self.assertTrue(key not in self.result)
