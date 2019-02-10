def is_valid_key(key):
    try:
        val = int(key)
        return True
    except ValueError:
        return False
    return False
