from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_organization_membership_body import UpdateOrganizationMembershipBody
from ...models.update_organization_membership_response_200 import UpdateOrganizationMembershipResponse200
from ...models.update_organization_membership_response_400 import UpdateOrganizationMembershipResponse400
from ...models.update_organization_membership_response_404 import UpdateOrganizationMembershipResponse404
from ...models.update_organization_membership_response_422 import UpdateOrganizationMembershipResponse422
from ...types import Response


def _get_kwargs(
    organization_id: str,
    user_id: str,
    *,
    body: UpdateOrganizationMembershipBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/organizations/{organization_id}/memberships/{user_id}",
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
        UpdateOrganizationMembershipResponse200,
        UpdateOrganizationMembershipResponse400,
        UpdateOrganizationMembershipResponse404,
        UpdateOrganizationMembershipResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateOrganizationMembershipResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateOrganizationMembershipResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateOrganizationMembershipResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateOrganizationMembershipResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateOrganizationMembershipResponse200,
        UpdateOrganizationMembershipResponse400,
        UpdateOrganizationMembershipResponse404,
        UpdateOrganizationMembershipResponse422,
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
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOrganizationMembershipBody,
) -> Response[
    Union[
        UpdateOrganizationMembershipResponse200,
        UpdateOrganizationMembershipResponse400,
        UpdateOrganizationMembershipResponse404,
        UpdateOrganizationMembershipResponse422,
    ]
]:
    """Update an organization membership

     Updates the properties of an existing organization membership

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOrganizationMembershipResponse200, UpdateOrganizationMembershipResponse400, UpdateOrganizationMembershipResponse404, UpdateOrganizationMembershipResponse422]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: str,
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOrganizationMembershipBody,
) -> Optional[
    Union[
        UpdateOrganizationMembershipResponse200,
        UpdateOrganizationMembershipResponse400,
        UpdateOrganizationMembershipResponse404,
        UpdateOrganizationMembershipResponse422,
    ]
]:
    """Update an organization membership

     Updates the properties of an existing organization membership

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOrganizationMembershipResponse200, UpdateOrganizationMembershipResponse400, UpdateOrganizationMembershipResponse404, UpdateOrganizationMembershipResponse422]
    """

    return sync_detailed(
        organization_id=organization_id,
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    organization_id: str,
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOrganizationMembershipBody,
) -> Response[
    Union[
        UpdateOrganizationMembershipResponse200,
        UpdateOrganizationMembershipResponse400,
        UpdateOrganizationMembershipResponse404,
        UpdateOrganizationMembershipResponse422,
    ]
]:
    """Update an organization membership

     Updates the properties of an existing organization membership

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOrganizationMembershipResponse200, UpdateOrganizationMembershipResponse400, UpdateOrganizationMembershipResponse404, UpdateOrganizationMembershipResponse422]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: str,
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateOrganizationMembershipBody,
) -> Optional[
    Union[
        UpdateOrganizationMembershipResponse200,
        UpdateOrganizationMembershipResponse400,
        UpdateOrganizationMembershipResponse404,
        UpdateOrganizationMembershipResponse422,
    ]
]:
    """Update an organization membership

     Updates the properties of an existing organization membership

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOrganizationMembershipResponse200, UpdateOrganizationMembershipResponse400, UpdateOrganizationMembershipResponse404, UpdateOrganizationMembershipResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
