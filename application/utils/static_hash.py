import hashlib
import os

_hash_cache = {}


def file_hash(static_folder, filepath):
    if filepath in _hash_cache:
        return _hash_cache[filepath]
    abs_path = os.path.join(static_folder, filepath)
    if not os.path.exists(abs_path):
        _hash_cache[filepath] = "na"
        return "na"
    with open(abs_path, "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()[:8]
    _hash_cache[filepath] = h
    return h


def register_bust(app):
    static_folder = app.static_folder

    def bust(filepath):
        return f"/static/{filepath}?v={file_hash(static_folder, filepath)}"

    app.jinja_env.globals["bust"] = bust
