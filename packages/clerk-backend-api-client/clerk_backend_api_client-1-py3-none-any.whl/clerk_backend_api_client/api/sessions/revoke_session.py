from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.revoke_session_response_200 import RevokeSessionResponse200
from ...models.revoke_session_response_400 import RevokeSessionResponse400
from ...models.revoke_session_response_401 import RevokeSessionResponse401
from ...models.revoke_session_response_404 import RevokeSessionResponse404
from ...types import Response


def _get_kwargs(
    session_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/sessions/{session_id}/revoke",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RevokeSessionResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RevokeSessionResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = RevokeSessionResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RevokeSessionResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
]:
    r"""Revoke a session

     Sets the status of a session as \"revoked\", which is an unauthenticated state.
    In multi-session mode, a revoked session will still be returned along with its client object,
    however the user will need to sign in again.

    Args:
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
]:
    r"""Revoke a session

     Sets the status of a session as \"revoked\", which is an unauthenticated state.
    In multi-session mode, a revoked session will still be returned along with its client object,
    however the user will need to sign in again.

    Args:
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
    """

    return sync_detailed(
        session_id=session_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
]:
    r"""Revoke a session

     Sets the status of a session as \"revoked\", which is an unauthenticated state.
    In multi-session mode, a revoked session will still be returned along with its client object,
    however the user will need to sign in again.

    Args:
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]]
    """

    kwargs = _get_kwargs(
        session_id=session_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    session_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
]:
    r"""Revoke a session

     Sets the status of a session as \"revoked\", which is an unauthenticated state.
    In multi-session mode, a revoked session will still be returned along with its client object,
    however the user will need to sign in again.

    Args:
        session_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeSessionResponse200, RevokeSessionResponse400, RevokeSessionResponse401, RevokeSessionResponse404]
    """

    return (
        await asyncio_detailed(
            session_id=session_id,
            client=client,
        )
    ).parsed
