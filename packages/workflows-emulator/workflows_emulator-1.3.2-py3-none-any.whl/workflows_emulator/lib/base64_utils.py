import base64


def decode(data: str, padding: bool = True) -> bytes:
    return base64.b64decode(data, validate=padding)

def encode(data: bytes, _padding: bool = True) -> str:
    return base64.b64encode(data).decode('utf-8')