# hash.py — simple hashing for testing

import hashlib

def get_password_hash(password: str) -> str:
    # hash with SHA256 (no 72-byte limit, secure enough for testing)
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password
