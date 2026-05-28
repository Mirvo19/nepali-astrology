import time

_store = {}


def get(key):
    entry = _store.get(key)
    if entry and time.time() < entry["expires"]:
        return entry["data"]
    return None


def set(key, data, ttl=300):
    _store[key] = {"data": data, "expires": time.time() + ttl}


def invalidate(key):
    _store.pop(key, None)


def invalidate_prefix(prefix):
    keys = [k for k in _store if k.startswith(prefix)]
    for k in keys:
        _store.pop(k, None)
