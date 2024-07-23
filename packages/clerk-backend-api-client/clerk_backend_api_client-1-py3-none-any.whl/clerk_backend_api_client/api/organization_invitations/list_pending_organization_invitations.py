from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_pending_organization_invitations_response_200 import ListPendingOrganizationInvitationsResponse200
from ...models.list_pending_organization_invitations_response_400 import ListPendingOrganizationInvitationsResponse400
from ...models.list_pending_organization_invitations_response_404 import ListPendingOrganizationInvitationsResponse404
from ...types import UNSET, Response, Unset


def _get_kwargs(
    organization_id: str,
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
        "url": f"/organizations/{organization_id}/invitations/pending",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ListPendingOrganizationInvitationsResponse200,
        ListPendingOrganizationInvitationsResponse400,
        ListPendingOrganizationInvitationsResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ListPendingOrganizationInvitationsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = ListPendingOrganizationInvitationsResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = ListPendingOrganizationInvitationsResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ListPendingOrganizationInvitationsResponse200,
        ListPendingOrganizationInvitationsResponse400,
        ListPendingOrganizationInvitationsResponse404,
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
) -> Response[
    Union[
        ListPendingOrganizationInvitationsResponse200,
        ListPendingOrganizationInvitationsResponse400,
        ListPendingOrganizationInvitationsResponse404,
    ]
]:
    r"""Get a list of pending organization invitations

     This request returns the list of organization invitations with \"pending\" status.
    These are the organization invitations that can still be used to join the organization, but have not
    been accepted by the invited user yet.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListPendingOrganizationInvitationsResponse200, ListPendingOrganizationInvitationsResponse400, ListPendingOrganizationInvitationsResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
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
) -> Optional[
    Union[
        ListPendingOrganizationInvitationsResponse200,
        ListPendingOrganizationInvitationsResponse400,
        ListPendingOrganizationInvitationsResponse404,
    ]
]:
    r"""Get a list of pending organization invitations

     This request returns the list of organization invitations with \"pending\" status.
    These are the organization invitations that can still be used to join the organization, but have not
    been accepted by the invited user yet.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListPendingOrganizationInvitationsResponse200, ListPendingOrganizationInvitationsResponse400, ListPendingOrganizationInvitationsResponse404]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        limit=limit,
        offset=offset,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Response[
    Union[
        ListPendingOrganizationInvitationsResponse200,
        ListPendingOrganizationInvitationsResponse400,
        ListPendingOrganizationInvitationsResponse404,
    ]
]:
    r"""Get a list of pending organization invitations

     This request returns the list of organization invitations with \"pending\" status.
    These are the organization invitations that can still be used to join the organization, but have not
    been accepted by the invited user yet.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ListPendingOrganizationInvitationsResponse200, ListPendingOrganizationInvitationsResponse400, ListPendingOrganizationInvitationsResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        limit=limit,
        offset=offset,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    limit: Union[Unset, float] = 10.0,
    offset: Union[Unset, float] = 0.0,
) -> Optional[
    Union[
        ListPendingOrganizationInvitationsResponse200,
        ListPendingOrganizationInvitationsResponse400,
        ListPendingOrganizationInvitationsResponse404,
    ]
]:
    r"""Get a list of pending organization invitations

     This request returns the list of organization invitations with \"pending\" status.
    These are the organization invitations that can still be used to join the organization, but have not
    been accepted by the invited user yet.
    Results can be paginated using the optional `limit` and `offset` query parameters.
    The organization invitations are ordered by descending creation date.
    Most recent invitations will be returned first.
    Any invitations created as a result of an Organization Domain are not included in the results.

    Args:
        organization_id (str):
        limit (Union[Unset, float]):  Default: 10.0.
        offset (Union[Unset, float]):  Default: 0.0.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ListPendingOrganizationInvitationsResponse200, ListPendingOrganizationInvitationsResponse400, ListPendingOrganizationInvitationsResponse404]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            limit=limit,
            offset=offset,
        )
    ).parsed
