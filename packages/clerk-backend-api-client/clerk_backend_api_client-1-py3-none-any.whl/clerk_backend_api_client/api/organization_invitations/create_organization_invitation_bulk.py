from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_organization_invitation_bulk_body_item import CreateOrganizationInvitationBulkBodyItem
from ...models.create_organization_invitation_bulk_response_200 import CreateOrganizationInvitationBulkResponse200
from ...models.create_organization_invitation_bulk_response_400 import CreateOrganizationInvitationBulkResponse400
from ...models.create_organization_invitation_bulk_response_403 import CreateOrganizationInvitationBulkResponse403
from ...models.create_organization_invitation_bulk_response_404 import CreateOrganizationInvitationBulkResponse404
from ...models.create_organization_invitation_bulk_response_422 import CreateOrganizationInvitationBulkResponse422
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    body: List["CreateOrganizationInvitationBulkBodyItem"],
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/organizations/{organization_id}/invitations/bulk",
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        CreateOrganizationInvitationBulkResponse200,
        CreateOrganizationInvitationBulkResponse400,
        CreateOrganizationInvitationBulkResponse403,
        CreateOrganizationInvitationBulkResponse404,
        CreateOrganizationInvitationBulkResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateOrganizationInvitationBulkResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateOrganizationInvitationBulkResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreateOrganizationInvitationBulkResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateOrganizationInvitationBulkResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateOrganizationInvitationBulkResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateOrganizationInvitationBulkResponse200,
        CreateOrganizationInvitationBulkResponse400,
        CreateOrganizationInvitationBulkResponse403,
        CreateOrganizationInvitationBulkResponse404,
        CreateOrganizationInvitationBulkResponse422,
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
    body: List["CreateOrganizationInvitationBulkBodyItem"],
) -> Response[
    Union[
        CreateOrganizationInvitationBulkResponse200,
        CreateOrganizationInvitationBulkResponse400,
        CreateOrganizationInvitationBulkResponse403,
        CreateOrganizationInvitationBulkResponse404,
        CreateOrganizationInvitationBulkResponse422,
    ]
]:
    r"""Bulk create and send organization invitations

     Creates new organization invitations in bulk and sends out emails to the provided email addresses
    with a link to accept the invitation and join the organization.
    You can specify a different `role` for each invited organization member.
    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.
    The request body supports passing an optional `redirect_url` parameter for each invitation.
    When the invited user clicks the link to accept the invitation, they will be redirected to the
    provided URL.
    Use this parameter to implement a custom invitation acceptance flow.
    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter. Each invitation
    can have a different inviter user.
    Inviter users must be members with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.
    You can optionally provide public and private metadata for each organization invitation. The public
    metadata are visible
    by both the Frontend and the Backend, whereas the private metadata are only visible by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (List['CreateOrganizationInvitationBulkBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationInvitationBulkResponse200, CreateOrganizationInvitationBulkResponse400, CreateOrganizationInvitationBulkResponse403, CreateOrganizationInvitationBulkResponse404, CreateOrganizationInvitationBulkResponse422]]
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
    body: List["CreateOrganizationInvitationBulkBodyItem"],
) -> Optional[
    Union[
        CreateOrganizationInvitationBulkResponse200,
        CreateOrganizationInvitationBulkResponse400,
        CreateOrganizationInvitationBulkResponse403,
        CreateOrganizationInvitationBulkResponse404,
        CreateOrganizationInvitationBulkResponse422,
    ]
]:
    r"""Bulk create and send organization invitations

     Creates new organization invitations in bulk and sends out emails to the provided email addresses
    with a link to accept the invitation and join the organization.
    You can specify a different `role` for each invited organization member.
    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.
    The request body supports passing an optional `redirect_url` parameter for each invitation.
    When the invited user clicks the link to accept the invitation, they will be redirected to the
    provided URL.
    Use this parameter to implement a custom invitation acceptance flow.
    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter. Each invitation
    can have a different inviter user.
    Inviter users must be members with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.
    You can optionally provide public and private metadata for each organization invitation. The public
    metadata are visible
    by both the Frontend and the Backend, whereas the private metadata are only visible by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (List['CreateOrganizationInvitationBulkBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationInvitationBulkResponse200, CreateOrganizationInvitationBulkResponse400, CreateOrganizationInvitationBulkResponse403, CreateOrganizationInvitationBulkResponse404, CreateOrganizationInvitationBulkResponse422]
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
    body: List["CreateOrganizationInvitationBulkBodyItem"],
) -> Response[
    Union[
        CreateOrganizationInvitationBulkResponse200,
        CreateOrganizationInvitationBulkResponse400,
        CreateOrganizationInvitationBulkResponse403,
        CreateOrganizationInvitationBulkResponse404,
        CreateOrganizationInvitationBulkResponse422,
    ]
]:
    r"""Bulk create and send organization invitations

     Creates new organization invitations in bulk and sends out emails to the provided email addresses
    with a link to accept the invitation and join the organization.
    You can specify a different `role` for each invited organization member.
    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.
    The request body supports passing an optional `redirect_url` parameter for each invitation.
    When the invited user clicks the link to accept the invitation, they will be redirected to the
    provided URL.
    Use this parameter to implement a custom invitation acceptance flow.
    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter. Each invitation
    can have a different inviter user.
    Inviter users must be members with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.
    You can optionally provide public and private metadata for each organization invitation. The public
    metadata are visible
    by both the Frontend and the Backend, whereas the private metadata are only visible by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (List['CreateOrganizationInvitationBulkBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationInvitationBulkResponse200, CreateOrganizationInvitationBulkResponse400, CreateOrganizationInvitationBulkResponse403, CreateOrganizationInvitationBulkResponse404, CreateOrganizationInvitationBulkResponse422]]
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
    body: List["CreateOrganizationInvitationBulkBodyItem"],
) -> Optional[
    Union[
        CreateOrganizationInvitationBulkResponse200,
        CreateOrganizationInvitationBulkResponse400,
        CreateOrganizationInvitationBulkResponse403,
        CreateOrganizationInvitationBulkResponse404,
        CreateOrganizationInvitationBulkResponse422,
    ]
]:
    r"""Bulk create and send organization invitations

     Creates new organization invitations in bulk and sends out emails to the provided email addresses
    with a link to accept the invitation and join the organization.
    You can specify a different `role` for each invited organization member.
    New organization invitations get a \"pending\" status until they are revoked by an organization
    administrator or accepted by the invitee.
    The request body supports passing an optional `redirect_url` parameter for each invitation.
    When the invited user clicks the link to accept the invitation, they will be redirected to the
    provided URL.
    Use this parameter to implement a custom invitation acceptance flow.
    You must specify the ID of the user that will send the invitation with the `inviter_user_id`
    parameter. Each invitation
    can have a different inviter user.
    Inviter users must be members with administrator privileges in the organization.
    Only \"admin\" members can create organization invitations.
    You can optionally provide public and private metadata for each organization invitation. The public
    metadata are visible
    by both the Frontend and the Backend, whereas the private metadata are only visible by the Backend.
    When the organization invitation is accepted, the metadata will be transferred to the newly created
    organization membership.

    Args:
        organization_id (str):
        body (List['CreateOrganizationInvitationBulkBodyItem']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationInvitationBulkResponse200, CreateOrganizationInvitationBulkResponse400, CreateOrganizationInvitationBulkResponse403, CreateOrganizationInvitationBulkResponse404, CreateOrganizationInvitationBulkResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
