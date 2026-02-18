def safe_int(value):
    try:
        return int(value)
    except:
        return 0


def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]
