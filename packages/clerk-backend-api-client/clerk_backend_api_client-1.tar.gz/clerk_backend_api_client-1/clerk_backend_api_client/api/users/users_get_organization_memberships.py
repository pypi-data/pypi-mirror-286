from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.users_get_organization_memberships_response_200 import UsersGetOrganizationMembershipsResponse200
from ...models.users_get_organization_memberships_response_403 import UsersGetOrganizationMembershipsResponse403
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
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
        "url": f"/users/{user_id}/organization_memberships",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UsersGetOrganizationMembershipsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UsersGetOrganizationMembershipsResponse403.from_dict(response.json())

        return response_403
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]:
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
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]:
    """Retrieve all memberships for a user

     Retrieve a paginated list of the user's organization memberships

    Args:
        user_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]:
    """Retrieve all memberships for a user

     Retrieve a paginated list of the user's organization memberships

    Args:
        user_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]:
    """Retrieve all memberships for a user

     Retrieve a paginated list of the user's organization memberships

    Args:
        user_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]]:
    """Retrieve all memberships for a user

     Retrieve a paginated list of the user's organization memberships

    Args:
        user_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UsersGetOrganizationMembershipsResponse200, UsersGetOrganizationMembershipsResponse403]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
