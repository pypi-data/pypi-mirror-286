from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_organization_invitation_body import CreateOrganizationInvitationBody
from ...models.create_organization_invitation_response_200 import CreateOrganizationInvitationResponse200
from ...models.create_organization_invitation_response_400 import CreateOrganizationInvitationResponse400
from ...models.create_organization_invitation_response_403 import CreateOrganizationInvitationResponse403
from ...models.create_organization_invitation_response_404 import CreateOrganizationInvitationResponse404
from ...models.create_organization_invitation_response_422 import CreateOrganizationInvitationResponse422
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    body: CreateOrganizationInvitationBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/organizations/{organization_id}/invitations",
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
        CreateOrganizationInvitationResponse200,
        CreateOrganizationInvitationResponse400,
        CreateOrganizationInvitationResponse403,
        CreateOrganizationInvitationResponse404,
        CreateOrganizationInvitationResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateOrganizationInvitationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateOrganizationInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreateOrganizationInvitationResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateOrganizationInvitationResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateOrganizationInvitationResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateOrganizationInvitationResponse200,
        CreateOrganizationInvitationResponse400,
        CreateOrganizationInvitationResponse403,
        CreateOrganizationInvitationResponse404,
        CreateOrganizationInvitationResponse422,
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
    body: CreateOrganizationInvitationBody,
) -> Response[
    Union[
        CreateOrganizationInvitationResponse200,
        CreateOrganizationInvitationResponse400,
        CreateOrganizationInvitationResponse403,
        CreateOrganizationInvitationResponse404,
        CreateOrganizationInvitationResponse422,
    ]
]:
    r"""Create and send an organization invitation

     Creates a new organization invitation and sends an email to the provided `email_address` with a link
    to accept the invitation and join the organization.
    You can specify the `role` for the invited organization member.

    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.

    The request body supports passing an optional `redirect_url` parameter.
    When the invited user clicks the link to accept the invitation, they will be redirected to the URL
    provided.
    Use this parameter to implement a custom invitation acceptance flow.

    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter.
    That user must be a member with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.

    You can optionally provide public and private metadata for the organization invitation.
    The public metadata are visible by both the Frontend and the Backend whereas the private ones only
    by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (CreateOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationInvitationResponse200, CreateOrganizationInvitationResponse400, CreateOrganizationInvitationResponse403, CreateOrganizationInvitationResponse404, CreateOrganizationInvitationResponse422]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOrganizationInvitationBody,
) -> Optional[
    Union[
        CreateOrganizationInvitationResponse200,
        CreateOrganizationInvitationResponse400,
        CreateOrganizationInvitationResponse403,
        CreateOrganizationInvitationResponse404,
        CreateOrganizationInvitationResponse422,
    ]
]:
    r"""Create and send an organization invitation

     Creates a new organization invitation and sends an email to the provided `email_address` with a link
    to accept the invitation and join the organization.
    You can specify the `role` for the invited organization member.

    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.

    The request body supports passing an optional `redirect_url` parameter.
    When the invited user clicks the link to accept the invitation, they will be redirected to the URL
    provided.
    Use this parameter to implement a custom invitation acceptance flow.

    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter.
    That user must be a member with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.

    You can optionally provide public and private metadata for the organization invitation.
    The public metadata are visible by both the Frontend and the Backend whereas the private ones only
    by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (CreateOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationInvitationResponse200, CreateOrganizationInvitationResponse400, CreateOrganizationInvitationResponse403, CreateOrganizationInvitationResponse404, CreateOrganizationInvitationResponse422]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOrganizationInvitationBody,
) -> Response[
    Union[
        CreateOrganizationInvitationResponse200,
        CreateOrganizationInvitationResponse400,
        CreateOrganizationInvitationResponse403,
        CreateOrganizationInvitationResponse404,
        CreateOrganizationInvitationResponse422,
    ]
]:
    r"""Create and send an organization invitation

     Creates a new organization invitation and sends an email to the provided `email_address` with a link
    to accept the invitation and join the organization.
    You can specify the `role` for the invited organization member.

    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.

    The request body supports passing an optional `redirect_url` parameter.
    When the invited user clicks the link to accept the invitation, they will be redirected to the URL
    provided.
    Use this parameter to implement a custom invitation acceptance flow.

    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter.
    That user must be a member with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.

    You can optionally provide public and private metadata for the organization invitation.
    The public metadata are visible by both the Frontend and the Backend whereas the private ones only
    by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (CreateOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationInvitationResponse200, CreateOrganizationInvitationResponse400, CreateOrganizationInvitationResponse403, CreateOrganizationInvitationResponse404, CreateOrganizationInvitationResponse422]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateOrganizationInvitationBody,
) -> Optional[
    Union[
        CreateOrganizationInvitationResponse200,
        CreateOrganizationInvitationResponse400,
        CreateOrganizationInvitationResponse403,
        CreateOrganizationInvitationResponse404,
        CreateOrganizationInvitationResponse422,
    ]
]:
    r"""Create and send an organization invitation

     Creates a new organization invitation and sends an email to the provided `email_address` with a link
    to accept the invitation and join the organization.
    You can specify the `role` for the invited organization member.

    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.

    The request body supports passing an optional `redirect_url` parameter.
    When the invited user clicks the link to accept the invitation, they will be redirected to the URL
    provided.
    Use this parameter to implement a custom invitation acceptance flow.

    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter.
    That user must be a member with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.

    You can optionally provide public and private metadata for the organization invitation.
    The public metadata are visible by both the Frontend and the Backend whereas the private ones only
    by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (CreateOrganizationInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationInvitationResponse200, CreateOrganizationInvitationResponse400, CreateOrganizationInvitationResponse403, CreateOrganizationInvitationResponse404, CreateOrganizationInvitationResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
