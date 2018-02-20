import unittest
import config
from modules import db
from modules.result import Result


class TestResult(unittest.TestCase):
    def setUp(self):
        db.get_users().delete_many({'username': 'test'})
        db.get_users().insert_one({'username': 'test', 'password': '123123', 'salt': 'salt'})

    def test(self):
        print("Hello")