import hashlib


def checksum(string):
    return hashlib.md5(string).hexdigest()
