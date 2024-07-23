from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_client_list_response_200_item import GetClientListResponse200Item
from ...models.get_client_list_response_400 import GetClientListResponse400
from ...models.get_client_list_response_401 import GetClientListResponse401
from ...models.get_client_list_response_410 import GetClientListResponse410
from ...models.get_client_list_response_422 import GetClientListResponse422
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/clients",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetClientListResponse400,
        GetClientListResponse401,
        GetClientListResponse410,
        GetClientListResponse422,
        List["GetClientListResponse200Item"],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetClientListResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetClientListResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetClientListResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.GONE:
        response_410 = GetClientListResponse410.from_dict(response.json())

        return response_410
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = GetClientListResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetClientListResponse400,
        GetClientListResponse401,
        GetClientListResponse410,
        GetClientListResponse422,
        List["GetClientListResponse200Item"],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        GetClientListResponse400,
        GetClientListResponse401,
        GetClientListResponse410,
        GetClientListResponse422,
        List["GetClientListResponse200Item"],
    ]
]:
    """List all clients

     Returns a list of all clients. The clients are returned sorted by creation date,
    with the newest clients appearing first.
    Warning: the endpoint is being deprecated and will be removed in future versions.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetClientListResponse400, GetClientListResponse401, GetClientListResponse410, GetClientListResponse422, List['GetClientListResponse200Item']]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        GetClientListResponse400,
        GetClientListResponse401,
        GetClientListResponse410,
        GetClientListResponse422,
        List["GetClientListResponse200Item"],
    ]
]:
    """List all clients

     Returns a list of all clients. The clients are returned sorted by creation date,
    with the newest clients appearing first.
    Warning: the endpoint is being deprecated and will be removed in future versions.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetClientListResponse400, GetClientListResponse401, GetClientListResponse410, GetClientListResponse422, List['GetClientListResponse200Item']]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        GetClientListResponse400,
        GetClientListResponse401,
        GetClientListResponse410,
        GetClientListResponse422,
        List["GetClientListResponse200Item"],
    ]
]:
    """List all clients

     Returns a list of all clients. The clients are returned sorted by creation date,
    with the newest clients appearing first.
    Warning: the endpoint is being deprecated and will be removed in future versions.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetClientListResponse400, GetClientListResponse401, GetClientListResponse410, GetClientListResponse422, List['GetClientListResponse200Item']]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        GetClientListResponse400,
        GetClientListResponse401,
        GetClientListResponse410,
        GetClientListResponse422,
        List["GetClientListResponse200Item"],
    ]
]:
    """List all clients

     Returns a list of all clients. The clients are returned sorted by creation date,
    with the newest clients appearing first.
    Warning: the endpoint is being deprecated and will be removed in future versions.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetClientListResponse400, GetClientListResponse401, GetClientListResponse410, GetClientListResponse422, List['GetClientListResponse200Item']]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
