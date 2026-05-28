import hashlib
import os
from flask import current_app

_hash_cache = {}


def file_hash(filepath):
    if filepath in _hash_cache:
        return _hash_cache[filepath]
    abs_path = os.path.join(current_app.static_folder, filepath)
    if not os.path.exists(abs_path):
        return ""
    with open(abs_path, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()[:8]
    _hash_cache[filepath] = h
    return h


def bust(filepath):
    return f"/static/{filepath}?v={file_hash(filepath)}"
