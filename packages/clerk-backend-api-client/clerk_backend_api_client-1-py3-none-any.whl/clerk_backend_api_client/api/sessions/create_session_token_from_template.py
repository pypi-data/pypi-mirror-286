from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_session_token_from_template_response_200 import CreateSessionTokenFromTemplateResponse200
from ...models.create_session_token_from_template_response_401 import CreateSessionTokenFromTemplateResponse401
from ...models.create_session_token_from_template_response_404 import CreateSessionTokenFromTemplateResponse404
from ...types import Response


def _get_kwargs(
    session_id: str,
    template_name: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/sessions/{session_id}/tokens/{template_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreateSessionTokenFromTemplateResponse200,
        CreateSessionTokenFromTemplateResponse401,
        CreateSessionTokenFromTemplateResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateSessionTokenFromTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = CreateSessionTokenFromTemplateResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateSessionTokenFromTemplateResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateSessionTokenFromTemplateResponse200,
        CreateSessionTokenFromTemplateResponse401,
        CreateSessionTokenFromTemplateResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    template_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        CreateSessionTokenFromTemplateResponse200,
        CreateSessionTokenFromTemplateResponse401,
        CreateSessionTokenFromTemplateResponse404,
    ]
]:
    """Create a session token from a jwt template

     Creates a JSON Web Token(JWT) based on a session and a JWT Template name defined for your instance

    Args:
        session_id (str):
        template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSessionTokenFromTemplateResponse200, CreateSessionTokenFromTemplateResponse401, CreateSessionTokenFromTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        template_name=template_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    template_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        CreateSessionTokenFromTemplateResponse200,
        CreateSessionTokenFromTemplateResponse401,
        CreateSessionTokenFromTemplateResponse404,
    ]
]:
    """Create a session token from a jwt template

     Creates a JSON Web Token(JWT) based on a session and a JWT Template name defined for your instance

    Args:
        session_id (str):
        template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSessionTokenFromTemplateResponse200, CreateSessionTokenFromTemplateResponse401, CreateSessionTokenFromTemplateResponse404]
    """

    return sync_detailed(
        session_id=session_id,
        template_name=template_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    template_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        CreateSessionTokenFromTemplateResponse200,
        CreateSessionTokenFromTemplateResponse401,
        CreateSessionTokenFromTemplateResponse404,
    ]
]:
    """Create a session token from a jwt template

     Creates a JSON Web Token(JWT) based on a session and a JWT Template name defined for your instance

    Args:
        session_id (str):
        template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSessionTokenFromTemplateResponse200, CreateSessionTokenFromTemplateResponse401, CreateSessionTokenFromTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
        template_name=template_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    template_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        CreateSessionTokenFromTemplateResponse200,
        CreateSessionTokenFromTemplateResponse401,
        CreateSessionTokenFromTemplateResponse404,
    ]
]:
    """Create a session token from a jwt template

     Creates a JSON Web Token(JWT) based on a session and a JWT Template name defined for your instance

    Args:
        session_id (str):
        template_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSessionTokenFromTemplateResponse200, CreateSessionTokenFromTemplateResponse401, CreateSessionTokenFromTemplateResponse404]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            template_name=template_name,
            client=client,
        )
    ).parsed
