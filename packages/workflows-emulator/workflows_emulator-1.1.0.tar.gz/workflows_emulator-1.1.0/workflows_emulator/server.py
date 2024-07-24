import json
import os
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from workflows_emulator.main import execute_workflow, load_workflow


class WorkflowExecutionRequest(BaseModel):
    argument: str = Field(default='{}')
    callLogLevel: str = Field(default='ALL')


def default_handler_clousure(workflow_path: str):
    def default_handler(
        body: WorkflowExecutionRequest,
        project_ref: str,
        location: str,
        workflow_id: str
    ):
        # reload config with every request
        workflow_config = load_workflow(workflow_path)
        # setup env vars
        if project_ref.isnumeric():
            os.environ['GOOGLE_CLOUD_PROJECT_NUMBER'] = project_ref
        else:
            os.environ['GOOGLE_CLOUD_PROJECT_ID'] = project_ref
        os.environ['GOOGLE_CLOUD_LOCATION'] = location
        os.environ['GOOGLE_CLOUD_WORKFLOW_ID'] = workflow_id
        # hash the workflow config to get the revision id
        from hashlib import sha256
        sha = sha256()
        sha.update(str(workflow_config).encode())
        revision_id = sha.hexdigest()[0:6]
        os.environ['GOOGLE_CLOUD_WORKFLOW_REVISION_ID'] = revision_id
        os.environ['GOOGLE_CLOUD_WORKFLOW_EXECUTION_ID'] = uuid.uuid4().hex
        # run the workflow
        params = json.loads(body.argument)
        outputs = execute_workflow(workflow_config, params)
        return outputs

    return default_handler
