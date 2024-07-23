from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_organization_invitation_response_200 import GetOrganizationInvitationResponse200
from ...models.get_organization_invitation_response_400 import GetOrganizationInvitationResponse400
from ...models.get_organization_invitation_response_403 import GetOrganizationInvitationResponse403
from ...models.get_organization_invitation_response_404 import GetOrganizationInvitationResponse404
from ...types import Response


def _get_kwargs(
    organization_id: str,
    invitation_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/organizations/{organization_id}/invitations/{invitation_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetOrganizationInvitationResponse200,
        GetOrganizationInvitationResponse400,
        GetOrganizationInvitationResponse403,
        GetOrganizationInvitationResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetOrganizationInvitationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetOrganizationInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = GetOrganizationInvitationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetOrganizationInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetOrganizationInvitationResponse200,
        GetOrganizationInvitationResponse400,
        GetOrganizationInvitationResponse403,
        GetOrganizationInvitationResponse404,
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
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetOrganizationInvitationResponse200,
        GetOrganizationInvitationResponse400,
        GetOrganizationInvitationResponse403,
        GetOrganizationInvitationResponse404,
    ]
]:
    """Retrieve an organization invitation by ID

     Use this request to get an existing organization invitation by ID.

    Args:
        organization_id (str):
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetOrganizationInvitationResponse200, GetOrganizationInvitationResponse400, GetOrganizationInvitationResponse403, GetOrganizationInvitationResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invitation_id=invitation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetOrganizationInvitationResponse200,
        GetOrganizationInvitationResponse400,
        GetOrganizationInvitationResponse403,
        GetOrganizationInvitationResponse404,
    ]
]:
    """Retrieve an organization invitation by ID

     Use this request to get an existing organization invitation by ID.

    Args:
        organization_id (str):
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetOrganizationInvitationResponse200, GetOrganizationInvitationResponse400, GetOrganizationInvitationResponse403, GetOrganizationInvitationResponse404]
    """

    return sync_detailed(
        organization_id=organization_id,
        invitation_id=invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetOrganizationInvitationResponse200,
        GetOrganizationInvitationResponse400,
        GetOrganizationInvitationResponse403,
        GetOrganizationInvitationResponse404,
    ]
]:
    """Retrieve an organization invitation by ID

     Use this request to get an existing organization invitation by ID.

    Args:
        organization_id (str):
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetOrganizationInvitationResponse200, GetOrganizationInvitationResponse400, GetOrganizationInvitationResponse403, GetOrganizationInvitationResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invitation_id=invitation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetOrganizationInvitationResponse200,
        GetOrganizationInvitationResponse400,
        GetOrganizationInvitationResponse403,
        GetOrganizationInvitationResponse404,
    ]
]:
    """Retrieve an organization invitation by ID

     Use this request to get an existing organization invitation by ID.

    Args:
        organization_id (str):
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetOrganizationInvitationResponse200, GetOrganizationInvitationResponse400, GetOrganizationInvitationResponse403, GetOrganizationInvitationResponse404]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            invitation_id=invitation_id,
            client=client,
        )
    ).parsed
