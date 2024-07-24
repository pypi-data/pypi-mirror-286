"""
Methods in this module mimic the original ones described in the docs,
but might not be 100% accurate. Some errors might not rise or some hidden
behavior might not be implemented.
"""
import os
from types import MappingProxyType
from typing import Any

from google.auth import default, impersonated_credentials
from google.auth.credentials import AnonymousCredentials, Credentials
from google.auth.transport.requests import AuthorizedSession

from workflows_emulator.lib.retry_utils import default_backoff
from workflows_emulator.utils import IMPERSONATED_SA, gen_retry_predicate

EmptyDict = MappingProxyType({})

default_retry_predicate = gen_retry_predicate(
    [429, 502, 503, 504],
    ['ConnectionError', 'ConnectionFailedError', 'TimeoutError']
)

default_retry_predicate_non_idempotent = gen_retry_predicate(
    [429, 503],
    ['ConnectionFailedError']
)

default_retry = {
    'predicate': default_retry_predicate,
    'max_retries': 5,
    'backoff': default_backoff,
}

default_retry_non_idempotent = {
    'predicate': default_retry_predicate_non_idempotent,
    'max_retries': 5,
    'backoff': default_backoff,
}


def delete(**kwargs) -> Any:
    return request('DELETE', **kwargs)


def get(**kwargs) -> Any:
    return request('GET', **kwargs)


def patch(**kwargs) -> Any:
    return request('PATCH', **kwargs)


def post(**kwargs) -> Any:
    return request('POST', **kwargs)


def put(**kwargs) -> Any:
    return request('PUT', **kwargs)


AUTH_OAUTH2 = {'type': 'OAuth2'}
AUTH_OIDC = {'type': 'OIDC'}


def request(
    method: str,
    url: str,
    timeout: float = 300,
    body: Any = None,
    headers: dict[str, str] = {},
    query: dict = {},
    auth: dict[str, dict[str, str]] = None,
    scopes: list[str] = ('https://www.googleapis.com/auth/cloud-platform',),
    private_service_name: str = None,
    ca_certificate: bytes = None,
):
    if private_service_name is not None:
        raise NotImplementedError('Private services are not supported yet.')
    if ca_certificate is not None:
        raise NotImplementedError(
            'Custom CA certificates are not supported yet.'
        )
    # determines the credentials to use
    credentials: Credentials = AnonymousCredentials()
    if auth:
        match auth['type']:
            case 'OIDC':
                raise NotImplementedError('OIDC auth is not supported yet.')
            case 'OAuth2':
                credentials, _project = default(scopes=scopes)

    # if impersonation is set, delegate to the impersonated service account
    impersonated_sa = os.getenv(IMPERSONATED_SA, None)
    if impersonated_sa is not None:
        credentials = impersonated_credentials.Credentials(
            source_credentials=credentials,
            target_principal=impersonated_sa,
            target_scopes=scopes
        )
    authed_session = AuthorizedSession(credentials)
    params = {}
    if isinstance(body, dict):
        params['json'] = body
    elif body:
        params['data'] = body

    resp = authed_session.request(
        method,
        url,
        headers=headers,
        timeout=timeout,
        params=query,
        **params,
    )

    resp.raise_for_status()

    if 'application/json' in resp.headers.get('Content-Type', ''):
        body = resp.json()
    else:
        body = resp.text

    return {
        'code': resp.status_code,
        'headers': dict(resp.headers),
        'body': body,
    }
