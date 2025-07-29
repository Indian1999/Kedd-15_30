dict = {
    "asd": 4,
    "bds": "cica"
}

import hashlib
import time
def code_timestamp(timestamp):
    hash_object = hashlib.sha256(str(timestamp).encode())
    return hash_object.hexdigest()

print(code_timestamp(0.0))
