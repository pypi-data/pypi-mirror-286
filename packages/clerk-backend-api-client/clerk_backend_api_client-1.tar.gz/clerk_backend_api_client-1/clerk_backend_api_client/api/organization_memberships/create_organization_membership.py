from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_organization_membership_body import CreateOrganizationMembershipBody
from ...models.create_organization_membership_response_200 import CreateOrganizationMembershipResponse200
from ...models.create_organization_membership_response_400 import CreateOrganizationMembershipResponse400
from ...models.create_organization_membership_response_403 import CreateOrganizationMembershipResponse403
from ...models.create_organization_membership_response_404 import CreateOrganizationMembershipResponse404
from ...models.create_organization_membership_response_422 import CreateOrganizationMembershipResponse422
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    body: CreateOrganizationMembershipBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/organizations/{organization_id}/memberships",
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
        CreateOrganizationMembershipResponse200,
        CreateOrganizationMembershipResponse400,
        CreateOrganizationMembershipResponse403,
        CreateOrganizationMembershipResponse404,
        CreateOrganizationMembershipResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = CreateOrganizationMembershipResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = CreateOrganizationMembershipResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = CreateOrganizationMembershipResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = CreateOrganizationMembershipResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = CreateOrganizationMembershipResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        CreateOrganizationMembershipResponse200,
        CreateOrganizationMembershipResponse400,
        CreateOrganizationMembershipResponse403,
        CreateOrganizationMembershipResponse404,
        CreateOrganizationMembershipResponse422,
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
    body: CreateOrganizationMembershipBody,
) -> Response[
    Union[
        CreateOrganizationMembershipResponse200,
        CreateOrganizationMembershipResponse400,
        CreateOrganizationMembershipResponse403,
        CreateOrganizationMembershipResponse404,
        CreateOrganizationMembershipResponse422,
    ]
]:
    """Create a new organization membership

     Adds a user as a member to the given organization.
    Only users in the same instance as the organization can be added as members.

    Args:
        organization_id (str):
        body (CreateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationMembershipResponse200, CreateOrganizationMembershipResponse400, CreateOrganizationMembershipResponse403, CreateOrganizationMembershipResponse404, CreateOrganizationMembershipResponse422]]
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
    body: CreateOrganizationMembershipBody,
) -> Optional[
    Union[
        CreateOrganizationMembershipResponse200,
        CreateOrganizationMembershipResponse400,
        CreateOrganizationMembershipResponse403,
        CreateOrganizationMembershipResponse404,
        CreateOrganizationMembershipResponse422,
    ]
]:
    """Create a new organization membership

     Adds a user as a member to the given organization.
    Only users in the same instance as the organization can be added as members.

    Args:
        organization_id (str):
        body (CreateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationMembershipResponse200, CreateOrganizationMembershipResponse400, CreateOrganizationMembershipResponse403, CreateOrganizationMembershipResponse404, CreateOrganizationMembershipResponse422]
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
    body: CreateOrganizationMembershipBody,
) -> Response[
    Union[
        CreateOrganizationMembershipResponse200,
        CreateOrganizationMembershipResponse400,
        CreateOrganizationMembershipResponse403,
        CreateOrganizationMembershipResponse404,
        CreateOrganizationMembershipResponse422,
    ]
]:
    """Create a new organization membership

     Adds a user as a member to the given organization.
    Only users in the same instance as the organization can be added as members.

    Args:
        organization_id (str):
        body (CreateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateOrganizationMembershipResponse200, CreateOrganizationMembershipResponse400, CreateOrganizationMembershipResponse403, CreateOrganizationMembershipResponse404, CreateOrganizationMembershipResponse422]]
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
    body: CreateOrganizationMembershipBody,
) -> Optional[
    Union[
        CreateOrganizationMembershipResponse200,
        CreateOrganizationMembershipResponse400,
        CreateOrganizationMembershipResponse403,
        CreateOrganizationMembershipResponse404,
        CreateOrganizationMembershipResponse422,
    ]
]:
    """Create a new organization membership

     Adds a user as a member to the given organization.
    Only users in the same instance as the organization can be added as members.

    Args:
        organization_id (str):
        body (CreateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateOrganizationMembershipResponse200, CreateOrganizationMembershipResponse400, CreateOrganizationMembershipResponse403, CreateOrganizationMembershipResponse404, CreateOrganizationMembershipResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
