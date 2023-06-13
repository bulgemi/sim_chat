from typing import Optional
from uuid import uuid4

import toml


config = toml.load("config.toml")
azure = config['azure']
huggingface = config['huggingface']

trn_id = f"trn-{uuid4()}"


def get_interface() -> dict:
    if 'azure' in config and config['azure']['use'] is True:
        return {'interface': 'azure', 'config': config['azure']}
    elif 'huggingface' in config and config['huggingface']['use'] is True:
        return {'interface': 'huggingface', 'config': config['huggingface']}


def get_openai_endpoint() -> Optional[str]:
    return f"https://{azure['openai_resource_name']}.openai.azure.com/openai/deployments/{azure['openai_deployment_name']}/{azure['operation_name']}?api-version={azure['api_version']}"


def get_header() -> Optional[dict]:
    headers = {
        "Content-Type": "application/json",
        "api-key": azure['api_key'],
        "trn-id": trn_id,
    }
    return headers


def get_huggingface_model() -> Optional[str]:
    return huggingface['model']
