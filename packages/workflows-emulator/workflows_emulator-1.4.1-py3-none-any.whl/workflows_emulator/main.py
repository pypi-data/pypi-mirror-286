import copy
import importlib
import json

import logging
import os
import pkgutil
from time import sleep
from typing import Dict, Optional

import yaml
from jsonschema import validate
from requests import HTTPError

from workflows_emulator.lib.http_utils import (
    AUTH_OAUTH2,
    request as authenticated_request,
)
from workflows_emulator.render import assign_var, render_config, run_code
from workflows_emulator.utils import DISCOVERY_DOCUMENTS_PATH, WorkflowException

logger = logging.getLogger('workflows')

# TODO: implement SafeLineLoader to enrich the error messages
# class SafeLineLoader(SafeLoader):
#     def construct_mapping(self, node, deep=False):
#         mapping = super(SafeLineLoader, self).construct_mapping(node,
#         deep=deep)
#         # Add 1 so line numbering starts at 1
#         mapping['__line__'] = node.start_mark.line + 1
#         return mapping

def load_config(config_path: str) -> dict:
    """Load a configuration file from a given path."""
    with open(config_path) as file:
        return yaml.safe_load(file)

def load_package_config(config_path: str) -> dict:
    """Load a configuration file from a given path inside the package."""
    package_path = importlib.resources.files(__package__)
    file_path = package_path / config_path
    with file_path.open() as file:
        return yaml.safe_load(file)


WORKFLOW_SCHEMA = load_package_config('workflow-schema.json')


def load_workflow(config_path: str) -> Dict:
    """Load a workflow from a given path."""
    workflow = load_config(config_path)
    validate(workflow, WORKFLOW_SCHEMA)
    return workflow


def execute_workflow(config: dict | list[dict], params: dict) -> any:
    """
    Runs a workflow given a configuration and parameters.

    We need the whole config inside the prams to run try/retry "predicate" and
    to be able to call other sub-workflows. Also, having it in the context is
    cleaner than storing it in a global variable
    """
    # if the root is a list of steps instead of a map with a 'main' key
    if isinstance(config, list):
        config = {'main': {'steps': config}}

    main_config = config.pop('main')
    logger.info(f"Running 'main' workflow: params -> {json.dumps(params)}")
    return execute_subworkflow(main_config, params, config)


def get_params(workflow_params: list[str | dict], runtime_params: dict) -> dict:
    context = {}
    for param in workflow_params:
        if isinstance(param, dict):
            param_name = list(param.keys())[0]
            param_value = param[param_name]
            context[param_name] = runtime_params.get(param_name, param_value)
        else:
            try:
                context[param] = runtime_params[param]
            except KeyError:
                raise KeyError(f"Missing workflow parameter: {param}")
    return context


def execute_subworkflow(workflow: dict, params: dict, context: dict) -> any:
    solved_params = get_params(workflow.get('params', []), params)
    logger.info(f"Running subworkflow")
    logger.debug(f"Subworkflow started: : params -> {json.dumps(solved_params)}")
    context.update(solved_params)
    _ctxt, next_step, ret_value = execute_steps_list(workflow['steps'], context)
    if next_step is not None:
        raise ValueError(f"Step {next_step} not found in the workflow")
    logger.info(f"Subworkflow complete: result -> {json.dumps(ret_value)}")
    return ret_value


def get_step(
    steps: list[dict], step_id: str
) -> tuple[str | None, int, dict]:
    """Returns the index of the step with the given id, or -1 if not found."""
    if step_id is None:
        step_id = list(steps[0].keys())[0]
        return step_id, 0, steps[0][step_id]
    for index, step in enumerate(steps):
        if list(step.keys())[0] == step_id:
            return step_id, index, step[step_id]
    return None, STEP_NOT_FOUND, {}


STEP_NOT_FOUND = -1

def execute_steps_list(
    steps: list[dict],
    context: dict,
    next_step: str = None,
) -> tuple[dict, str | None, any]:
    """
    It either returns a context and a ret_value or a step_id to go to and
    continue execution

    Returns:
    - context: The context after executing the steps
    - next_step: The step id to go to, or None to continue with the next step
    - ret_value: The return value of the steps
    """
    ret_value = None
    while True:
        if next_step == 'end':
            return context, None, None
        step_id, step_index, step_config = get_step(steps, next_step)
        # if the next_step was SET but NOT FOUND, return to search in the parent
        if step_index == STEP_NOT_FOUND:
            break
        logger.info(f"Step running: `{step_id}`")
        context, next_step, ret_value = execute_step(step_config, context)
        if ret_value is not None:
            break
        # if the step did not return a next_step, get the next step in the list
        if next_step is None:
            if step_index + 1 < len(steps):
                next_step = list(steps[step_index + 1].keys())[0]
            else:
                break
        # if the list returned a next_step, will be used in the next iteration
    return context, next_step, ret_value


def execute_step(step: dict, context: dict) -> tuple[dict, Optional[str], any]:
    """Executes the step and returns the context and, if any, the result and
    return value

    Returns:
    - context: The context after executing the step
    - next: None to go to the next step, or the step id to go to a specific step
    - return: The return value of the step
    """
    no_next_step = None
    no_return_value = None
    logger.debug(f"  Step type: {'/'.join(step.keys())}")
    try:
        match list(step.keys()):
            case ['call', *_]:
                result_context = execute_step_call(step, context)
                return result_context, no_next_step, no_return_value
            case ['return']:
                ret_value = render_config(step['return'], context)
                return context, no_next_step, ret_value
            case ['assign']:
                result_context = execute_step_assign(step['assign'], context)
                return result_context, no_next_step, no_return_value
            case ['raise']:
                execute_step_raise(step, context)
            case ['try', 'except']:
                return execute_step_try(step, context)
            case ['try', 'retry', *_]:
                return execute_step_retry(step, context)
            case ['steps']:
                return execute_step_steps(step['steps'], context)
            case ['for']:
                return execute_step_for(step['for'], context)
            case ['next']:
                # `next: end` is a special case to finish the workflow
                return context, step['next'], no_return_value
            case ['parallel']:
                result_context = execute_step_parallel(step['parallel'],
                                                       context)
                return result_context, no_next_step, no_return_value
            case ['switch', *_]:
                return execute_step_switch(step, context)
            case unknown:
                raise ValueError(f"Unknown step type: {unknown}")
    except WorkflowException as err:
        raise err
    except (
        ConnectionError, TypeError, ValueError, KeyError,
        SystemError, TimeoutError, IndexError, RecursionError, ZeroDivisionError
    ) as err:
        raise WorkflowException(
            message=err.args[0],
            tags=[err.__class__.__name__],
        )
    except HTTPError as err:
        body = err.response.text
        if 'application/json' in err.response.headers.get('Content-Type', ''):
            body = err.response.json()
        raise WorkflowException(
            message=err.args[0],
            tags=[err.__class__.__name__],
            code=err.response.status_code,
            headers=dict(err.response.headers),
            body=body,
        )


def execute_step_for(step: dict, context: dict) -> tuple[dict, str | None, any]:
    if 'in' in step:
        iterable = render_config(step['in'], context)
    else:
        iterable_range = render_config(step['range'])
        iterable = range(*iterable_range)
    index_variable = step.get('index', '__index')
    value_variable = step.get('value', '__value')
    next_step = None
    ret_value = None
    for index, value in enumerate(iterable):
        context[index_variable] = index
        context[value_variable] = value
        context, next_step, ret_value = execute_step_steps(
            step['steps'],
            context
        )
        if ret_value is not None or next_step is not None:
            break
    context.pop(index_variable)
    context.pop(value_variable)
    return context, next_step, ret_value

def execute_step_raise(step: dict, context: dict) -> None:
    rendered_error = render_config(step['raise'], context)
    # suppose that the error is a string by default
    error_map = {
        'message': rendered_error,
        'tags': ['WorkflowException'],
    }
    # if it was a dictionary use it instead
    if isinstance(rendered_error, dict):
        error_map = rendered_error

    raise WorkflowException(
        **error_map,
    )


def execute_step_try(step: dict, context: dict) -> tuple[dict, str, any]:
    try:
        return execute_step(step['try'], context)
    except WorkflowException as err:
        error_var = step['except']['as']
        context[error_var] = err.map
        return execute_steps_list(step['except']['steps'], context)


def keep_only_subworkflows(context: dict) -> dict:
    return {
        key: value
        for key, value in context.items()
        if isinstance(value, dict) and 'steps' in value
    }

def execute_step_retry(
    step: dict,
    context: dict
) -> tuple[dict, Optional[str], any]:
    retry_config = render_config(step['retry'], context)
    if 'backoff' in retry_config:
        backoff_config = retry_config['backoff']
        delay = backoff_config['initial_delay']
        max_delay = backoff_config['max_delay']
        multiplier = backoff_config['initial_delay']
    predicate = retry_config.get('predicate', None)
    raised_err = None
    for retry_num in range(retry_config['max_retries'] + 1):
        try:
            if retry_num > 0:
                logger.debug(f"Retry -> Attempt {retry_num}")
            return execute_step(step['try'], context)
        except WorkflowException as err:
            raised_err = err
            # do the sleep
            if 'backoff' in retry_config:
                logger.debug(f"Retry -> waiting {delay} seconds")
                if delay < max_delay:
                    sleep(delay)
                    delay *= multiplier
                # we run out of time but the issue was not fixed
                else:
                    logger.error(f"Retry -> timeout. Max delay {max_delay} "
                                 f"reached.")
                    raise err
            # check if we need to execute the predicate
            if predicate is not None:
                logger.info(f"Retry -> Running predicate")
                run_result = execute_subworkflow(
                    workflow=predicate,
                    params={'e': err.map},
                    context=keep_only_subworkflows(context)
                )
                # if the handling was successful it returned True
                if isinstance(run_result, bool) and run_result:
                    break
    else:
        # if retries run out, but not the max_delay and the predicate didn't
        # fix it
        logger.info(f"Retry -> Max retries reached or predicate failed.")
        if 'except' in step:
            error_var = step['except']['as']
            context[error_var] = raised_err.map
            return execute_steps_list(step['except']['steps'], context)
        else:
            raise raised_err
    return context, None, None


def execute_step_steps(
    step: list[dict],
    context: dict
) -> tuple[dict, str, any]:
    """Ensures that inner variables do not bleed out of context."""
    context_copy = copy.deepcopy(context)
    new_context, next_step, ret_value = execute_steps_list(step, context_copy)
    context = {
        key: new_context.get(key, value)
        for key, value in context.items()
    }
    return context, next_step, ret_value


def execute_step_assign(vars: list[dict], context: dict) -> dict:
    for var in vars:
        var_name = list(var.keys())[0]
        var_value = var[var_name]
        rendered_value = render_config(var_value, context)
        root_key, new_val = assign_var(var_name, rendered_value, context)
        context[root_key] = new_val
    return context


def execute_step_call_connector(rendered_step: dict) -> dict:
    # @formatter:off
    _, service_name, version, *resources, method = rendered_step['call'].split('.')

    service_discovery_file_path = f'{DISCOVERY_DOCUMENTS_PATH}/{service_name}_{version}.json'

    service_discovery_config = load_package_config(service_discovery_file_path)
    # iteratively consume the parts to get the final config
    next_part = service_discovery_config
    for resource in resources:
        next_part = next_part['resources'][resource]
    final_config = next_part['methods'][method]

    # now that we have the actual method config, extract the information
    scopes = final_config['scopes']
    http_verb = final_config['httpMethod']
    base_url = service_discovery_config['rootUrl']
    config_path = final_config['path'].replace('+', '')
    service_path = service_discovery_config['servicePath']
    final_url_template = base_url + service_path + config_path
    final_url = eval(f'f"""{final_url_template}"""', rendered_step['args'])
    # make the request
    result = authenticated_request(
        url=final_url,
        auth=AUTH_OAUTH2,
        body=rendered_step['args'].get('body', None),
        method=http_verb,
        scopes=scopes
    )
    return result['body']


def execute_step_call(step: dict, context: dict) -> dict:
    rendered_step = render_config(step, context)
    callable_name = rendered_step['call']
    logger.debug(f"  Calling: {callable_name}")
    if callable_name.startswith('googleapis.'):
        run_result = execute_step_call_connector(rendered_step)
    # call another subworkflow
    elif callable_name in context:
        run_result = execute_subworkflow(
            workflow=context[callable_name],
            params=rendered_step.get('args', {}),
            context=keep_only_subworkflows(context)
        )
        logger.info(f"Finished subworkflow: {callable_name} with result {str(run_result)}")
    # call a python function from the standard libraby
    else:
        fn_args = rendered_step.get('args', {})
        args_str = "**_args" if isinstance(fn_args, dict) else "*_args"
        run_result = run_code(
            code=f'{callable_name}({args_str})',
            context={**context, '_args': fn_args}
        )
    if 'result' in rendered_step:
        context[step['result']] = run_result
    return context


def execute_step_parallel(step: dict, context: dict) -> dict:
    if 'for' in step:
        context, next_step, _ret_value = execute_step_for(step['for'], context)
    # if not 'for', then it is 'branches'
    else:
        context, next_step, _ret_value = execute_step_steps(
            step['branches'],
            context
        )
    if next_step is not None:
        raise ValueError(
            f"Cannot use `next: {next_step}` pointing outside the parallel step"
        )
    return context


def execute_step_switch(
    step: dict, context: dict
) -> tuple[dict, Optional[str], any]:
    for condition in step['switch']:
        # evaluate the condition and remove the field
        condition_copy = copy.deepcopy(condition)
        evaluated_condition = render_config(
            condition_copy['condition'],
            context
        )
        if not isinstance(evaluated_condition, bool):
            raise ValueError(
                f'The switch condition must evaluate to a boolean: `'
                f'{condition_copy["condition"]}`'
            )
        if evaluated_condition:
            condition_copy.pop('condition')
            context, next_step, ret_value = execute_step(
                condition_copy,
                context
            )
            if ret_value is not None or next_step is not None:
                return context, next_step, ret_value
    if 'next' in step:
        return context, step['next'], None

    return context, None, None
