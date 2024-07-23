from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_invitation_body import CreateInvitationBody
from ...models.create_invitation_response_200 import CreateInvitationResponse200
from ...models.create_invitation_response_400 import CreateInvitationResponse400
from ...models.create_invitation_response_422 import CreateInvitationResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: CreateInvitationBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/invitations",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateInvitationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateInvitationResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateInvitationResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateInvitationBody,
) -> Response[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]:
    """Create an invitation

     Creates a new invitation for the given email address and sends the invitation email.
    Keep in mind that you cannot create an invitation if there is already one for the given email
    address.
    Also, trying to create an invitation for an email address that already exists in your application
    will result to an error.

    Args:
        body (CreateInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateInvitationBody,
) -> Optional[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]:
    """Create an invitation

     Creates a new invitation for the given email address and sends the invitation email.
    Keep in mind that you cannot create an invitation if there is already one for the given email
    address.
    Also, trying to create an invitation for an email address that already exists in your application
    will result to an error.

    Args:
        body (CreateInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateInvitationBody,
) -> Response[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]:
    """Create an invitation

     Creates a new invitation for the given email address and sends the invitation email.
    Keep in mind that you cannot create an invitation if there is already one for the given email
    address.
    Also, trying to create an invitation for an email address that already exists in your application
    will result to an error.

    Args:
        body (CreateInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateInvitationBody,
) -> Optional[Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]]:
    """Create an invitation

     Creates a new invitation for the given email address and sends the invitation email.
    Keep in mind that you cannot create an invitation if there is already one for the given email
    address.
    Also, trying to create an invitation for an email address that already exists in your application
    will result to an error.

    Args:
        body (CreateInvitationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateInvitationResponse200, CreateInvitationResponse400, CreateInvitationResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
