from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.revoke_invitation_response_200 import RevokeInvitationResponse200
from ...models.revoke_invitation_response_400 import RevokeInvitationResponse400
from ...models.revoke_invitation_response_404 import RevokeInvitationResponse404
from ...types import Response


def _get_kwargs(
    invitation_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/invitations/{invitation_id}/revoke",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RevokeInvitationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RevokeInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RevokeInvitationResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]:
    """Revokes an invitation

     Revokes the given invitation.
    Revoking an invitation will prevent the user from using the invitation link that was sent to them.
    However, it doesn't prevent the user from signing up if they follow the sign up flow.
    Only active (i.e. non-revoked) invitations can be revoked.

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]
    """

    kwargs = _get_kwargs(
        invitation_id=invitation_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]:
    """Revokes an invitation

     Revokes the given invitation.
    Revoking an invitation will prevent the user from using the invitation link that was sent to them.
    However, it doesn't prevent the user from signing up if they follow the sign up flow.
    Only active (i.e. non-revoked) invitations can be revoked.

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]
    """

    return sync_detailed(
        invitation_id=invitation_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]:
    """Revokes an invitation

     Revokes the given invitation.
    Revoking an invitation will prevent the user from using the invitation link that was sent to them.
    However, it doesn't prevent the user from signing up if they follow the sign up flow.
    Only active (i.e. non-revoked) invitations can be revoked.

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]
    """

    kwargs = _get_kwargs(
        invitation_id=invitation_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    invitation_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]]:
    """Revokes an invitation

     Revokes the given invitation.
    Revoking an invitation will prevent the user from using the invitation link that was sent to them.
    However, it doesn't prevent the user from signing up if they follow the sign up flow.
    Only active (i.e. non-revoked) invitations can be revoked.

    Args:
        invitation_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevokeInvitationResponse200, RevokeInvitationResponse400, RevokeInvitationResponse404]
    """

    return (
        await asyncio_detailed(
            invitation_id=invitation_id,
            client=client,
        )
    ).parsed
