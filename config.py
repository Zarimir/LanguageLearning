class Rest():
    def __init__(self):
        self.index = "/"
        self.root_bare = "rest/"
        self.root = self.index + self.root_bare


rest = Rest()

collections = 'collections'
database = 'study'

# Constants
username_length = 3
password_length = 8
password_length_max = 72 # bcrypt hashing limit


# Fail messages
username_taken = 'username_taken'
invalid_username = 'invalid_username'
invalid_password = 'invalid_password'
internal_error = 'internal_error'
account_found = 'account_found'
login_error = 'login_error'
