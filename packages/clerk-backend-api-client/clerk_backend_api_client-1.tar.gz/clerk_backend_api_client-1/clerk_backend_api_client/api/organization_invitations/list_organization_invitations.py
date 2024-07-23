from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_organization_invitations_response_200 import ListOrganizationInvitationsResponse200
from ...models.list_organization_invitations_response_400 import ListOrganizationInvitationsResponse400
from ...models.list_organization_invitations_response_404 import ListOrganizationInvitationsResponse404
from ...models.list_organization_invitations_status import ListOrganizationInvitationsStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: str,
    *,
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    status: Union[Unset, ListOrganizationInvitationsStatus] = UNSET,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["limit"] = limit

    params["offset"] = offset

    json_status: Union[Unset, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value

    params["status"] = json_status

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/organizations/{organization_id}/invitations",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ListOrganizationInvitationsResponse200,
        ListOrganizationInvitationsResponse400,
        ListOrganizationInvitationsResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListOrganizationInvitationsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListOrganizationInvitationsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListOrganizationInvitationsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ListOrganizationInvitationsResponse200,
        ListOrganizationInvitationsResponse400,
        ListOrganizationInvitationsResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    status: Union[Unset, ListOrganizationInvitationsStatus] = UNSET,
) -> Response[
    Union[
        ListOrganizationInvitationsResponse200,
        ListOrganizationInvitationsResponse400,
        ListOrganizationInvitationsResponse404,
    ]
]:
    """Get a list of organization invitations

     This request returns the list of organization invitations.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    You can filter them by providing the 'status' query parameter, that accepts multiple values.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        status (Union[Unset, ListOrganizationInvitationsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListOrganizationInvitationsResponse200, ListOrganizationInvitationsResponse400, ListOrganizationInvitationsResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
        status=status,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    status: Union[Unset, ListOrganizationInvitationsStatus] = UNSET,
) -> Optional[
    Union[
        ListOrganizationInvitationsResponse200,
        ListOrganizationInvitationsResponse400,
        ListOrganizationInvitationsResponse404,
    ]
]:
    """Get a list of organization invitations

     This request returns the list of organization invitations.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    You can filter them by providing the 'status' query parameter, that accepts multiple values.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        status (Union[Unset, ListOrganizationInvitationsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListOrganizationInvitationsResponse200, ListOrganizationInvitationsResponse400, ListOrganizationInvitationsResponse404]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        limit=limit,
        offset=offset,
        status=status,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    status: Union[Unset, ListOrganizationInvitationsStatus] = UNSET,
) -> Response[
    Union[
        ListOrganizationInvitationsResponse200,
        ListOrganizationInvitationsResponse400,
        ListOrganizationInvitationsResponse404,
    ]
]:
    """Get a list of organization invitations

     This request returns the list of organization invitations.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    You can filter them by providing the 'status' query parameter, that accepts multiple values.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        status (Union[Unset, ListOrganizationInvitationsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListOrganizationInvitationsResponse200, ListOrganizationInvitationsResponse400, ListOrganizationInvitationsResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
        status=status,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
    status: Union[Unset, ListOrganizationInvitationsStatus] = UNSET,
) -> Optional[
    Union[
        ListOrganizationInvitationsResponse200,
        ListOrganizationInvitationsResponse400,
        ListOrganizationInvitationsResponse404,
    ]
]:
    """Get a list of organization invitations

     This request returns the list of organization invitations.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    You can filter them by providing the 'status' query parameter, that accepts multiple values.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.
        status (Union[Unset, ListOrganizationInvitationsStatus]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListOrganizationInvitationsResponse200, ListOrganizationInvitationsResponse400, ListOrganizationInvitationsResponse404]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            limit=limit,
            offset=offset,
            status=status,
        )
    ).parsed
