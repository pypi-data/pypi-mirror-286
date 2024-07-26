import json
import logging
import os

import click
import coloredlogs
import uvicorn
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI

from workflows_emulator.main import execute_workflow, load_workflow
from workflows_emulator.server import default_handler_clousure
from workflows_emulator.utils import IMPERSONATED_SA


WORKFLOW_EXECUTE_ROUTE = (
    "/v1/projects/{project_ref}/locations/{location}/workflows/{workflow_id}"
    "/executions"
)

@click.group(help='Command line interface for the Workflows emulator')
@click.option('--source', help='Path to the yaml config file')
@click.option(
    '--env-file',
    default='.env',
    show_default=True,
    help='Path to the `dot-env` file. Default is .env, so if you have a .env '
         'file in the current directory, you do not need to specify this '
         'argument'
)
@click.option(
    '--impersonate',
    help='Email of the service account to impersonate. It can also be read '
         'from the `IMPERSONATED_SA` environment variable'
)
@click.option(
    '--loglevel',
    default='INFO',
    show_default=True,
    type=click.Choice(
        [
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL', 'NOTICE', 'ALERT',
            'EMERGENCY'
        ],
    ),

    help='Provide logging level. Example --loglevel debug, default=warning'
)
@click.pass_context
def cli(ctx, source, env_file, impersonate, loglevel):
    logging.basicConfig(level=loglevel)
    coloredlogs.install(
        fmt="[%(asctime)s] %(name)s [%(levelname)s] %(message)s",
        level=loglevel,
        datefmt='%I:%M:%S',
    )

    ctx.ensure_object(dict)
    load_dotenv(env_file)
    ctx.obj['workflow_path'] = source
    if impersonate:
        os.environ[IMPERSONATED_SA] = impersonate


@cli.command(
    help='Input data for the workflow, either a path to the data or the '
         'actual data in yaml/json'
)
@click.option(
    '--data',
    help='Input data for the workflow, either a path to the data or the '
         'actual data in yaml/json'
)
@click.pass_context
def run(ctx, data):
    workflow_path = ctx.obj['workflow_path']
    workflow_config = load_workflow(workflow_path)
    params = {}
    if data:
        if os.path.isfile(data):
            with open(data) as params_file:
                params = yaml.safe_load(params_file)
        else:
            params = yaml.safe_load(data)

    outputs = execute_workflow(workflow_config, params)
    if isinstance(outputs, dict) or isinstance(outputs, list):
        outputs = json.dumps(outputs, indent=2)
    print(outputs)


@cli.command(
    help='Serve a workflow as a REST API. It accepts http requests on '
         'http://localhost:{port}/v1/projects/{project_ref}/locations/{'
         'location}/workflows/{workflow_id}/executions. Params will be '
         'extracted from the URL so that they will be available as ENV '
         'variableswhen the workflow is executed (see '
         'https://cloud.google.com/workflows/docs/reference/environment'
         '-variables). The `project_ref` can either be the `project_id` or '
         'the `project_number`. If it is numeric the later will be defined '
         'instead. To trigger it call the URL with a GET request and attach '
         'the params as a serialized JSON.'
)
@click.option(
    '--port',
    default=8000,
    show_default=True,
    type=int,
    help='Port to run the server on. Default is 8000'
)
@click.pass_context
def serve(ctx, port):
    workflow_path = ctx.obj['workflow_path']
    app = FastAPI()
    app.add_api_route(
        path=WORKFLOW_EXECUTE_ROUTE,
        endpoint=default_handler_clousure(workflow_path),
        methods=['POST']
    )
    startup_message = (
        f'Waiting for requests on http://localhost:{port}/v1/projects/'
        '{project_ref}/locations/{location}/workflows/{workflow_id}/executions'
    )
    app.add_event_handler('startup', lambda: logging.info(startup_message))

    uvicorn.run(app, host="0.0.0.0", port=port)
