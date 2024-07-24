"""
Methods in this module mimic the original ones described in the docs,
but might not be 100% accurate. Some errors might not rise or some hidden
behavior might not be implemented.
"""

# noinspection PyUnresolvedReferences
from urllib.parse import (
    quote as url_encode,
    quote_plus as url_encode_plus,
    unquote as url_decode,
)

import re2 as re


def decode(data: bytes, charset: str = 'utf-8') -> str:
    return data.decode(charset)


def encode(source: str, charset: str = 'utf-8') -> bytes:
    return source.encode(charset)


def find_all(source: str, substr: str) -> list[int]:
    return [m.start() for m in re.finditer(substr, source)]


def find_all_regex(source: str, regexp: str) -> list[int]:
    return [match.start() for match in re.finditer(regexp, source)]


def match_regex(source: str, regexp: str) -> bool:
    return bool(re.search(regexp, source))


def replace_all(source: str, substr: str, repl: str) -> str:
    return source.replace(substr, repl)


def replace_all_regex(source: str, regexp: str, repl: str) -> str:
    return re.sub(regexp, repl, source)


def split(source: str, separator: str) -> list[str]:
    return source.split(separator)


def substring(source: str, start: int, end: int) -> str:
    return source[start:end]


def to_upper(source: str) -> str:
    return source.upper()


def to_lower(source: str) -> str:
    return source.lower()
