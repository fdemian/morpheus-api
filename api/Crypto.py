import bcrypt

def hash_password(password):
    default_rounds = 14
    bcrypt_salt = bcrypt.gensalt(default_rounds)
    hashed_password = bcrypt.hashpw(password, bcrypt_salt)
    return hashed_password

def check_password(password, hashed):
    return bcrypt.checkpw(password, hashed)
