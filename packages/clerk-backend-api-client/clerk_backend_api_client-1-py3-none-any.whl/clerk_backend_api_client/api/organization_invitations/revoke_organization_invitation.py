from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.revoke_organization_invitation_body import RevokeOrganizationInvitationBody
from ...models.revoke_organization_invitation_response_200 import RevokeOrganizationInvitationResponse200
from ...models.revoke_organization_invitation_response_400 import RevokeOrganizationInvitationResponse400
from ...models.revoke_organization_invitation_response_403 import RevokeOrganizationInvitationResponse403
from ...models.revoke_organization_invitation_response_404 import RevokeOrganizationInvitationResponse404
from ...types import Response


def _get_kwargs(
    organization_id: str,
    invitation_id: str,
    *,
    body: RevokeOrganizationInvitationBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/organizations/{organization_id}/invitations/{invitation_id}/revoke",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        RevokeOrganizationInvitationResponse200,
        RevokeOrganizationInvitationResponse400,
        RevokeOrganizationInvitationResponse403,
        RevokeOrganizationInvitationResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RevokeOrganizationInvitationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RevokeOrganizationInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = RevokeOrganizationInvitationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RevokeOrganizationInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        RevokeOrganizationInvitationResponse200,
        RevokeOrganizationInvitationResponse400,
        RevokeOrganizationInvitationResponse403,
        RevokeOrganizationInvitationResponse404,
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
    body: RevokeOrganizationInvitationBody,
) -> Response[
    Union[
        RevokeOrganizationInvitationResponse200,
        RevokeOrganizationInvitationResponse400,
        RevokeOrganizationInvitationResponse403,
        RevokeOrganizationInvitationResponse404,
    ]
]:
    r"""Revoke a pending organization invitation

     Use this request to revoke a previously issued organization invitation.
    Revoking an organization invitation makes it invalid; the invited user will no longer be able to
    join the organization with the revoked invitation.
    Only organization invitations with \"pending\" status can be revoked.
    The request needs the `requesting_user_id` parameter to specify the user which revokes the
    invitation.
    Only users with \"admin\" role can revoke invitations.

    Args:
        organization_id (str):
        invitation_id (str):
        body (RevokeOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeOrganizationInvitationResponse200, RevokeOrganizationInvitationResponse400, RevokeOrganizationInvitationResponse403, RevokeOrganizationInvitationResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invitation_id=invitation_id,
        body=body,
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
    body: RevokeOrganizationInvitationBody,
) -> Optional[
    Union[
        RevokeOrganizationInvitationResponse200,
        RevokeOrganizationInvitationResponse400,
        RevokeOrganizationInvitationResponse403,
        RevokeOrganizationInvitationResponse404,
    ]
]:
    r"""Revoke a pending organization invitation

     Use this request to revoke a previously issued organization invitation.
    Revoking an organization invitation makes it invalid; the invited user will no longer be able to
    join the organization with the revoked invitation.
    Only organization invitations with \"pending\" status can be revoked.
    The request needs the `requesting_user_id` parameter to specify the user which revokes the
    invitation.
    Only users with \"admin\" role can revoke invitations.

    Args:
        organization_id (str):
        invitation_id (str):
        body (RevokeOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeOrganizationInvitationResponse200, RevokeOrganizationInvitationResponse400, RevokeOrganizationInvitationResponse403, RevokeOrganizationInvitationResponse404]
    """

    return sync_detailed(
        organization_id=organization_id,
        invitation_id=invitation_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RevokeOrganizationInvitationBody,
) -> Response[
    Union[
        RevokeOrganizationInvitationResponse200,
        RevokeOrganizationInvitationResponse400,
        RevokeOrganizationInvitationResponse403,
        RevokeOrganizationInvitationResponse404,
    ]
]:
    r"""Revoke a pending organization invitation

     Use this request to revoke a previously issued organization invitation.
    Revoking an organization invitation makes it invalid; the invited user will no longer be able to
    join the organization with the revoked invitation.
    Only organization invitations with \"pending\" status can be revoked.
    The request needs the `requesting_user_id` parameter to specify the user which revokes the
    invitation.
    Only users with \"admin\" role can revoke invitations.

    Args:
        organization_id (str):
        invitation_id (str):
        body (RevokeOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeOrganizationInvitationResponse200, RevokeOrganizationInvitationResponse400, RevokeOrganizationInvitationResponse403, RevokeOrganizationInvitationResponse404]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        invitation_id=invitation_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: RevokeOrganizationInvitationBody,
) -> Optional[
    Union[
        RevokeOrganizationInvitationResponse200,
        RevokeOrganizationInvitationResponse400,
        RevokeOrganizationInvitationResponse403,
        RevokeOrganizationInvitationResponse404,
    ]
]:
    r"""Revoke a pending organization invitation

     Use this request to revoke a previously issued organization invitation.
    Revoking an organization invitation makes it invalid; the invited user will no longer be able to
    join the organization with the revoked invitation.
    Only organization invitations with \"pending\" status can be revoked.
    The request needs the `requesting_user_id` parameter to specify the user which revokes the
    invitation.
    Only users with \"admin\" role can revoke invitations.

    Args:
        organization_id (str):
        invitation_id (str):
        body (RevokeOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeOrganizationInvitationResponse200, RevokeOrganizationInvitationResponse400, RevokeOrganizationInvitationResponse403, RevokeOrganizationInvitationResponse404]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            invitation_id=invitation_id,
            client=client,
            body=body,
        )
    ).parsed
