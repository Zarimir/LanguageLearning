import unittest
import config
from modules import db
from modules.account import *
from modules.result import Result


class TestResult(unittest.TestCase):
    def setUp(self):
        self.crash = {}
        self.invalid_username = 'AO@$!@%UY*Y2'
        self.invalid_password = '12'
        self.valid_username = 'test'
        self.valid_password = '123123'
        self.result = Result()
        self.user = {'username': self.valid_username, 'password': self.valid_password, 'salt': 'salt'}
        db.cleanup()
        db.get_users().delete_many({'username': self.user['username']})
        db.get_users().insert_one(self.user)

    def tearDown(self):
        db.cleanup()
        db.get_users().delete_many({'username': self.valid_username})

    def test_replace(self):
        account = db.get_users().find_one({'username': self.valid_username})
        attempt = replace(account)
        self.assertTrue(attempt)
        self.assertTrue(attempt['modified'] == 0)

        account['username'] = account['username'] + account['username']
        attempt = replace(account)
        self.assertTrue(attempt)
        self.assertTrue(attempt['modified'] == 1)

        account['username'] = self.invalid_username
        attempt = replace(account)
        self.assertFalse(attempt)
        self.assertTrue(attempt[config.invalid_username])

        account['username'] = self.valid_username
        account['password'] = self.invalid_password
        attempt = replace(account)
        self.assertFalse(attempt)
        self.assertTrue(attempt[config.invalid_password])

    def test_delete(self):
        attempt = delete({})
        self.assertTrue(attempt.crashed())

        attempt = delete({'username': self.valid_username})
        self.assertTrue(attempt)
        self.assertTrue(attempt['deleted'] == 1)

        attempt = delete({'username': self.valid_username})
        self.assertTrue(attempt)
        self.assertTrue(attempt['deleted'] == 0)

    def test_login_username(self):
        attempt = login(self.crash)
        self.assertTrue(attempt.crashed())

        attempt = login({'username': self.invalid_username})
        self.assertFalse(attempt)
        self.assertTrue(config.invalid_username in attempt)
        self.assertTrue(attempt[config.invalid_username])

        db.get_users().delete_many({'username': self.valid_username})
        attempt = login({'username': self.valid_username})
        self.assertFalse(attempt)
        self.assertTrue(config.account_found in attempt)
        self.assertFalse(attempt[config.account_found])

        self.setUp()
        attempt = login({'username': self.valid_username})
        self.assertTrue(attempt)
        self.assertTrue(config.account_found in attempt)
        self.assertTrue(attempt[config.account_found])

    def test_login_password(self):
        self.setUp()
        attempt = login(self.crash, password=True)
        self.assertTrue(attempt.crashed())

        attempt = login({'username': self.valid_username}, password=True)
        self.assertFalse(attempt)
        self.assertTrue(attempt[config.internal_error])

        attempt = login({'username': self.valid_username, 'password': self.invalid_password}, password=True)
        self.assertFalse(attempt)
        self.assertTrue(attempt[config.invalid_password])

        attempt = login({'username': self.valid_username, 'password': self.valid_password}, password=True)
        self.assertTrue(attempt)
        self.assertTrue(attempt[config.account_found])
        self.assertFalse(attempt[config.invalid_password])
