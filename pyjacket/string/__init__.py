def ensure_endswith(s: str, extension: str):
    return s if s.endswith(extension) else s + extension