import builtins
import copy
import json
import logging
import re
from typing import Any, Type, TypeVar

import typeguard
import yaml

from workflows_emulator.utils import DictNoDefault

logger = logging.getLogger()

# install typeguard import hook to check types on the std library functions
# it must be run before importing the standard library modules
typeguard.install_import_hook(
    [
        'lib_http', 'lib_sys', 'lib_text', 'lib_base64', 'lib_json', 'lib_list',
        'lib_map', 'lib_math', 'lib_time', 'lib_uuid', 'lib_retry'
    ]
)

import workflows_emulator.lib.http_utils as lib_http
import workflows_emulator.lib.sys_utils as lib_sys
import workflows_emulator.lib.text_utils as lib_text
import workflows_emulator.lib.base64_utils as lib_base64
import workflows_emulator.lib.json_utils as lib_json
import workflows_emulator.lib.list_utils as lib_list
import workflows_emulator.lib.map_utils as lib_map
import workflows_emulator.lib.math_utils as lib_math
import workflows_emulator.lib.time_utils as lib_time
import workflows_emulator.lib.uuid_utils as lib_uuid
import workflows_emulator.lib.retry_utils as lib_retry
from workflows_emulator.lib.helpers import helpers

STANDARD_LIBRARY = {
    'sys': lib_sys,
    'http': lib_http,
    'text': lib_text,
    'base64': lib_base64,
    'json': lib_json,
    'list': lib_list,
    'map': lib_map,
    'math': lib_math,
    'time': lib_time,
    'uuid': lib_uuid,
    'retry': lib_retry,
    **helpers,
}

CODE_PATTERN = re.compile(r'\${(.*?)}')


def run_code(code: str, context: dict) -> Any:
    """Run a code snippet in the given context"""

    # isolate the context so eval doesn't modify it
    context_copy = DictNoDefault(copy.deepcopy(context))
    # turn dictionaries into attribute-accessible dicts
    context_copy.update(STANDARD_LIBRARY)
    try:
        return eval(code, context_copy)
    # capture all exceptions from evaluating code and re-raise them
    except Exception as err:
        logger.error(
            f'Error evaulating code\nCode: `{code}`'
            f'\nContext:{json.dumps(context, indent=2)}'
            f'\nError: {err.__class__.__name__}: {err.args[0]}'
        )
        raise err


def assign_var(key: str, value: any, context: dict) -> tuple[str, any]:
    """
    Assign a value to a key in the context.
    Returns a dictionary with a single key-value pair, being the one assigned
    """

    # isolate the context so eval doesn't modify it
    context_copy = DictNoDefault(copy.deepcopy(context))
    # turn dictionaries into attribute-accessible dicts
    context_copy.update(STANDARD_LIBRARY)
    context_copy['__value'] = value
    code = f'{key} = __value'
    try:
        exec(code, context_copy)
        # key might be in the form of `key.subkey` or `key['other']`. Take the
        # first part of the key to get from the context
        key_root = re.search(r'^[^\[\.]+', key).group(0)
        return key_root, context_copy[key_root]
    # capture all exceptions from evaluating code and re-raise them
    except Exception as err:
        logger.error(
            f'Error executing code\nCode: `{code}`'
            f'\nContext:{json.dumps(context, indent=2)}'
            f'\nError: {err.__class__.__name__}: {err.args[0]}'
        )
        raise err


def render_str(value: str, context: dict) -> Any:
    """Render a field with ${} interpolation in the following steps:
    1. Extract the ${} patterns
    2. Run them through the context
    3. Replace the results in the original string
    4. Parse the result string as a yaml
    """
    # detect cases where it's not necessary to parse
    if not isinstance(value, str):
        return value
    if '${' not in value:
        return value

    # if the value is a scalar, it should be parsed as a string, not yaml
    eval_type = None

    def replace_match(match):
        code = match.group(1)
        evaluated = run_code(code, context)
        nonlocal eval_type
        eval_type = type(evaluated)
        # serialize non-raw types as yaml, they will probably be
        # the only element in the `value` to interpolate
        if eval_type in (list, dict):
            return json.dumps(evaluated)
        return str(evaluated)

    substituted, num_subs = re.subn(CODE_PATTERN, replace_match, value)

    # If there's more than one substitution the output is going to be a string
    # If the type is not a string, either ints, floats and others,
    # deserialization will behave correctly:
    #
    # | More than one substitution | Type is NOT string | parse |
    # |----------------------------|--------------------|-------|
    # | TRUE                       | TRUE               | NO    |
    # | TRUE                       | FALSE              | NO    |
    # | FALSE                      | TRUE               | NO    |
    # | FALSE                      | FALSE              | YES   |
    if num_subs == 1 and eval_type is not str:
        return yaml.safe_load(substituted)
    return substituted


ConfigType = TypeVar('ConfigType')


def render_config(
    config: Type[ConfigType],
    context: dict = {}
) -> ConfigType:
    """Recursively call render on all the leaf nodes"""
    match type(config):
        case builtins.str:
            return render_str(config, context)
        case builtins.dict:
            return {
                key: render_config(value, context)
                for key, value in config.items()
            }
        case builtins.list:
            return [
                render_config(item, context)
                for item in config
            ]
        case _:
            return config
