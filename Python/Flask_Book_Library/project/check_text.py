FORBIDDEN_CHARS = set('<>"\'`&/\\{};=')

def check_text(value, max_len=100):
    value = (value or "").strip()
    if not value or len(value) > max_len:
        raise ValueError("Niepoprawna długość")
    bad = FORBIDDEN_CHARS.intersection(value)
    if bad:
        raise ValueError(f"Niedozwolone znaki: {' '.join(sorted(bad))}")
    return value