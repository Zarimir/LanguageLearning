def gensalt():
    return "salt"

def hashpwd(string, hash):
    return string

def hashcmp(unhashed, hashed, salt):
    print(unhashed)
    print(hashed)
    return unhashed == hashed
