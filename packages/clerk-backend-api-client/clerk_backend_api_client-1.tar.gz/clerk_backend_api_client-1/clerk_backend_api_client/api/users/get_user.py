from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_user_response_200 import GetUserResponse200
from ...models.get_user_response_400 import GetUserResponse400
from ...models.get_user_response_401 import GetUserResponse401
from ...models.get_user_response_404 import GetUserResponse404
from ...types import Response


def _get_kwargs(
    user_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/users/{user_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetUserResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetUserResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetUserResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetUserResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]:
    """Retrieve a user

     Retrieve the details of a user

    Args:
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]:
    """Retrieve a user

     Retrieve the details of a user

    Args:
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]:
    """Retrieve a user

     Retrieve the details of a user

    Args:
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]]:
    """Retrieve a user

     Retrieve the details of a user

    Args:
        user_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetUserResponse200, GetUserResponse400, GetUserResponse401, GetUserResponse404]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
        )
    ).parsed
