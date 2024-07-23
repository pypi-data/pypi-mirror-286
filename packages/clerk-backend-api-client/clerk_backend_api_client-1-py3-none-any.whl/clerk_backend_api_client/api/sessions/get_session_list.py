from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_session_list_response_200_item import GetSessionListResponse200Item
from ...models.get_session_list_response_400 import GetSessionListResponse400
from ...models.get_session_list_response_401 import GetSessionListResponse401
from ...models.get_session_list_response_422 import GetSessionListResponse422
from ...models.get_session_list_status import GetSessionListStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client_id: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    status: Union[Unset, GetSessionListStatus] = UNSET,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["client_id"] = client_id

    params["user_id"] = user_id

    json_status: Union[Unset, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params["limit"] = limit

    params["offset"] = offset

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/sessions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetSessionListResponse400,
        GetSessionListResponse401,
        GetSessionListResponse422,
        List["GetSessionListResponse200Item"],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetSessionListResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetSessionListResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetSessionListResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = GetSessionListResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetSessionListResponse400,
        GetSessionListResponse401,
        GetSessionListResponse422,
        List["GetSessionListResponse200Item"],
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
    client_id: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    status: Union[Unset, GetSessionListStatus] = UNSET,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        GetSessionListResponse400,
        GetSessionListResponse401,
        GetSessionListResponse422,
        List["GetSessionListResponse200Item"],
    ]
]:
    """List all sessions

     Returns a list of all sessions.
    The sessions are returned sorted by creation date, with the newest sessions appearing first.
    **Deprecation Notice (2024-01-01):** All parameters were initially considered optional, however
    moving forward at least one of `client_id` or `user_id` parameters should be provided.

    Args:
        client_id (Union[Unset, str]):
        user_id (Union[Unset, str]):
        status (Union[Unset, GetSessionListStatus]):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSessionListResponse400, GetSessionListResponse401, GetSessionListResponse422, List['GetSessionListResponse200Item']]]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        user_id=user_id,
        status=status,
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
    client_id: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    status: Union[Unset, GetSessionListStatus] = UNSET,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        GetSessionListResponse400,
        GetSessionListResponse401,
        GetSessionListResponse422,
        List["GetSessionListResponse200Item"],
    ]
]:
    """List all sessions

     Returns a list of all sessions.
    The sessions are returned sorted by creation date, with the newest sessions appearing first.
    **Deprecation Notice (2024-01-01):** All parameters were initially considered optional, however
    moving forward at least one of `client_id` or `user_id` parameters should be provided.

    Args:
        client_id (Union[Unset, str]):
        user_id (Union[Unset, str]):
        status (Union[Unset, GetSessionListStatus]):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSessionListResponse400, GetSessionListResponse401, GetSessionListResponse422, List['GetSessionListResponse200Item']]
    """

    return sync_detailed(
        client=client,
        client_id=client_id,
        user_id=user_id,
        status=status,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    status: Union[Unset, GetSessionListStatus] = UNSET,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        GetSessionListResponse400,
        GetSessionListResponse401,
        GetSessionListResponse422,
        List["GetSessionListResponse200Item"],
    ]
]:
    """List all sessions

     Returns a list of all sessions.
    The sessions are returned sorted by creation date, with the newest sessions appearing first.
    **Deprecation Notice (2024-01-01):** All parameters were initially considered optional, however
    moving forward at least one of `client_id` or `user_id` parameters should be provided.

    Args:
        client_id (Union[Unset, str]):
        user_id (Union[Unset, str]):
        status (Union[Unset, GetSessionListStatus]):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSessionListResponse400, GetSessionListResponse401, GetSessionListResponse422, List['GetSessionListResponse200Item']]]
    """

    kwargs = _get_kwargs(
        client_id=client_id,
        user_id=user_id,
        status=status,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    client_id: Union[Unset, str] = UNSET,
    user_id: Union[Unset, str] = UNSET,
    status: Union[Unset, GetSessionListStatus] = UNSET,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        GetSessionListResponse400,
        GetSessionListResponse401,
        GetSessionListResponse422,
        List["GetSessionListResponse200Item"],
    ]
]:
    """List all sessions

     Returns a list of all sessions.
    The sessions are returned sorted by creation date, with the newest sessions appearing first.
    **Deprecation Notice (2024-01-01):** All parameters were initially considered optional, however
    moving forward at least one of `client_id` or `user_id` parameters should be provided.

    Args:
        client_id (Union[Unset, str]):
        user_id (Union[Unset, str]):
        status (Union[Unset, GetSessionListStatus]):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSessionListResponse400, GetSessionListResponse401, GetSessionListResponse422, List['GetSessionListResponse200Item']]
    """

    return (
        await asyncio_detailed(
            client=client,
            client_id=client_id,
            user_id=user_id,
            status=status,
            limit=limit,
            offset=offset,
        )
    ).parsed
