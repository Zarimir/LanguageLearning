class Rest():
    def __init__(self):
        self.index = "/"
        self.root = self.index + "rest/"
        self.users = self.root + "users"
        self.languages = self.root + "languages"
        self.words = self.root + "words"




rest = Rest()

collections = 'collections'
database = 'study'
users = 'users'
languages = 'languages'
words = 'words'
# Constants
username_length = 3
password_length = 8
password_length_max = 72 # bcrypt hashing limit


# Session key values
course = 'course'
language = 'language'
heading_to = 'heading_to'


# Fail messages
username_taken = 'username_taken'
invalid_username = 'invalid_username'
invalid_password = 'invalid_password'
internal_error = 'internal_error'
account_found = 'account_found'
login_error = 'login_error'
