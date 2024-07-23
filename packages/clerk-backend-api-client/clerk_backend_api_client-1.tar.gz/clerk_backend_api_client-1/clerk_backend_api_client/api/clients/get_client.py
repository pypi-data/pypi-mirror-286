from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_client_response_200 import GetClientResponse200
from ...models.get_client_response_400 import GetClientResponse400
from ...models.get_client_response_401 import GetClientResponse401
from ...models.get_client_response_404 import GetClientResponse404
from ...types import Response


def _get_kwargs(
    client_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/clients/{client_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetClientResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetClientResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetClientResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetClientResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    client_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]:
    """Get a client

     Returns the details of a client.

    Args:
        client_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    client_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]:
    """Get a client

     Returns the details of a client.

    Args:
        client_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]
    """

    return sync_detailed(
        client_id=client_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    client_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]:
    """Get a client

     Returns the details of a client.

    Args:
        client_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    client_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]]:
    """Get a client

     Returns the details of a client.

    Args:
        client_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetClientResponse200, GetClientResponse400, GetClientResponse401, GetClientResponse404]
    """

    return (
        await asyncio_detailed(
            client_id=client_id,
            client=client,
        )
    ).parsed
