def require_value(value, name: str):
    if value is None:
        raise ValueError(f"{name} is required")
    if isinstance(value, str) and not value.strip():
        raise ValueError(f"{name} is required")

