import hashlib

def hash256(string):
    "Two rounds of SHA256"
    return hashlib.sha256(hashlib.sha256(string).digest()).digest()