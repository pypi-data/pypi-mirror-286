from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_organizations_response_200 import ListOrganizationsResponse200
from ...models.list_organizations_response_400 import ListOrganizationsResponse400
from ...models.list_organizations_response_403 import ListOrganizationsResponse403
from ...models.list_organizations_response_422 import ListOrganizationsResponse422
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    include_members_count: Union[Unset, bool] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = "-created_at",
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    params["include_members_count"] = include_members_count

    params["query"] = query

    params["order_by"] = order_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/organizations",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ListOrganizationsResponse200,
        ListOrganizationsResponse400,
        ListOrganizationsResponse403,
        ListOrganizationsResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListOrganizationsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListOrganizationsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = ListOrganizationsResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = ListOrganizationsResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ListOrganizationsResponse200,
        ListOrganizationsResponse400,
        ListOrganizationsResponse403,
        ListOrganizationsResponse422,
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
    include_members_count: Union[Unset, bool] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = "-created_at",
) -> Response[
    Union[
        ListOrganizationsResponse200,
        ListOrganizationsResponse400,
        ListOrganizationsResponse403,
        ListOrganizationsResponse422,
    ]
]:
    """Get a list of organizations for an instance

     This request returns the list of organizations for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organizations are ordered by descending creation date.
    Most recent organizations will be returned first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        include_members_count (Union[Unset, bool]):
        query (Union[Unset, str]):
        order_by (Union[Unset, str]):  Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListOrganizationsResponse200, ListOrganizationsResponse400, ListOrganizationsResponse403, ListOrganizationsResponse422]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        include_members_count=include_members_count,
        query=query,
        order_by=order_by,
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
    include_members_count: Union[Unset, bool] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = "-created_at",
) -> Optional[
    Union[
        ListOrganizationsResponse200,
        ListOrganizationsResponse400,
        ListOrganizationsResponse403,
        ListOrganizationsResponse422,
    ]
]:
    """Get a list of organizations for an instance

     This request returns the list of organizations for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organizations are ordered by descending creation date.
    Most recent organizations will be returned first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        include_members_count (Union[Unset, bool]):
        query (Union[Unset, str]):
        order_by (Union[Unset, str]):  Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListOrganizationsResponse200, ListOrganizationsResponse400, ListOrganizationsResponse403, ListOrganizationsResponse422]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        include_members_count=include_members_count,
        query=query,
        order_by=order_by,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    include_members_count: Union[Unset, bool] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = "-created_at",
) -> Response[
    Union[
        ListOrganizationsResponse200,
        ListOrganizationsResponse400,
        ListOrganizationsResponse403,
        ListOrganizationsResponse422,
    ]
]:
    """Get a list of organizations for an instance

     This request returns the list of organizations for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organizations are ordered by descending creation date.
    Most recent organizations will be returned first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        include_members_count (Union[Unset, bool]):
        query (Union[Unset, str]):
        order_by (Union[Unset, str]):  Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListOrganizationsResponse200, ListOrganizationsResponse400, ListOrganizationsResponse403, ListOrganizationsResponse422]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        include_members_count=include_members_count,
        query=query,
        order_by=order_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    include_members_count: Union[Unset, bool] = UNSET,
    query: Union[Unset, str] = UNSET,
    order_by: Union[Unset, str] = "-created_at",
) -> Optional[
    Union[
        ListOrganizationsResponse200,
        ListOrganizationsResponse400,
        ListOrganizationsResponse403,
        ListOrganizationsResponse422,
    ]
]:
    """Get a list of organizations for an instance

     This request returns the list of organizations for an instance.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organizations are ordered by descending creation date.
    Most recent organizations will be returned first.

    Args:
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        include_members_count (Union[Unset, bool]):
        query (Union[Unset, str]):
        order_by (Union[Unset, str]):  Default: '-created_at'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListOrganizationsResponse200, ListOrganizationsResponse400, ListOrganizationsResponse403, ListOrganizationsResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            include_members_count=include_members_count,
            query=query,
            order_by=order_by,
        )
    ).parsed
