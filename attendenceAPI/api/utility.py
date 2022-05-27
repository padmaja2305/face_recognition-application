import hashlib
def hashpass(password):
    return hashlib.sha256(password.encode()).hexdigest()