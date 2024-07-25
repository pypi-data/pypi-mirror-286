import json


def decode(data: bytes | str, ) -> str:
    return json.loads(data)


DEFAULT_INDENT_CONFIG = {
    "prefix": "",
    "indent": 4
}


def encode(data: any, indent: bool | dict = DEFAULT_INDENT_CONFIG) -> bytes:
    """
    If indent is provided, it must be either a boolean, or a dictionary with
    two optional string attributes: prefix (defaulting to an empty string),
    and indent (defaulting to four spaces). Setting indent to true is
    equivalent to setting it to an empty dictionary. Setting indent to false
    is equivalent to not setting it.

    default_indent_config = {
        "prefix": "",
        "indent": 4
    }

    When the indentation is enabled, each JSON element begins on a new line
    beginning with prefix and followed by zero or more copies of indent
    according to the structural nesting.
    """
    aux_indent = DEFAULT_INDENT_CONFIG['indent']
    aux_prefix = DEFAULT_INDENT_CONFIG['prefix']
    if isinstance(indent, bool):
        if not indent:
            aux_indent = None
    elif isinstance(indent, dict):
        aux_indent = indent.get('indent', DEFAULT_INDENT_CONFIG['indent'])
        aux_prefix = indent.get('prefix', DEFAULT_INDENT_CONFIG['prefix'])

    stringified = json.dumps(data, indent=aux_indent)
    prefixed = [
        aux_prefix + line
        for line in stringified.splitlines()
    ]
    return '\n'.join(prefixed).encode()


def encode_to_string(
    data: any,
    indent: bool | dict = DEFAULT_INDENT_CONFIG
) -> str:
    return encode(data, indent).decode()
