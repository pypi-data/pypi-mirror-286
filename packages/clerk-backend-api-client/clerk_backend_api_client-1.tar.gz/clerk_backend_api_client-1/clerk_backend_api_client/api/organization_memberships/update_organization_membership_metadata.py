from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_organization_membership_metadata_body import UpdateOrganizationMembershipMetadataBody
from ...models.update_organization_membership_metadata_response_200 import (
    UpdateOrganizationMembershipMetadataResponse200,
)
from ...models.update_organization_membership_metadata_response_400 import (
    UpdateOrganizationMembershipMetadataResponse400,
)
from ...models.update_organization_membership_metadata_response_404 import (
    UpdateOrganizationMembershipMetadataResponse404,
)
from ...models.update_organization_membership_metadata_response_422 import (
    UpdateOrganizationMembershipMetadataResponse422,
)
from ...types import Response


def _get_kwargs(
    organization_id: str,
    user_id: str,
    *,
    body: UpdateOrganizationMembershipMetadataBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/organizations/{organization_id}/memberships/{user_id}/metadata",
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
        UpdateOrganizationMembershipMetadataResponse200,
        UpdateOrganizationMembershipMetadataResponse400,
        UpdateOrganizationMembershipMetadataResponse404,
        UpdateOrganizationMembershipMetadataResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateOrganizationMembershipMetadataResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateOrganizationMembershipMetadataResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateOrganizationMembershipMetadataResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateOrganizationMembershipMetadataResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateOrganizationMembershipMetadataResponse200,
        UpdateOrganizationMembershipMetadataResponse400,
        UpdateOrganizationMembershipMetadataResponse404,
        UpdateOrganizationMembershipMetadataResponse422,
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
    body: UpdateOrganizationMembershipMetadataBody,
) -> Response[
    Union[
        UpdateOrganizationMembershipMetadataResponse200,
        UpdateOrganizationMembershipMetadataResponse400,
        UpdateOrganizationMembershipMetadataResponse404,
        UpdateOrganizationMembershipMetadataResponse422,
    ]
]:
    """Merge and update organization membership metadata

     Update an organization membership's metadata attributes by merging existing values with the provided
    parameters.
    Metadata values will be updated via a deep merge. Deep means that any nested JSON objects will be
    merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOrganizationMembershipMetadataResponse200, UpdateOrganizationMembershipMetadataResponse400, UpdateOrganizationMembershipMetadataResponse404, UpdateOrganizationMembershipMetadataResponse422]]
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
    body: UpdateOrganizationMembershipMetadataBody,
) -> Optional[
    Union[
        UpdateOrganizationMembershipMetadataResponse200,
        UpdateOrganizationMembershipMetadataResponse400,
        UpdateOrganizationMembershipMetadataResponse404,
        UpdateOrganizationMembershipMetadataResponse422,
    ]
]:
    """Merge and update organization membership metadata

     Update an organization membership's metadata attributes by merging existing values with the provided
    parameters.
    Metadata values will be updated via a deep merge. Deep means that any nested JSON objects will be
    merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOrganizationMembershipMetadataResponse200, UpdateOrganizationMembershipMetadataResponse400, UpdateOrganizationMembershipMetadataResponse404, UpdateOrganizationMembershipMetadataResponse422]
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
    body: UpdateOrganizationMembershipMetadataBody,
) -> Response[
    Union[
        UpdateOrganizationMembershipMetadataResponse200,
        UpdateOrganizationMembershipMetadataResponse400,
        UpdateOrganizationMembershipMetadataResponse404,
        UpdateOrganizationMembershipMetadataResponse422,
    ]
]:
    """Merge and update organization membership metadata

     Update an organization membership's metadata attributes by merging existing values with the provided
    parameters.
    Metadata values will be updated via a deep merge. Deep means that any nested JSON objects will be
    merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOrganizationMembershipMetadataResponse200, UpdateOrganizationMembershipMetadataResponse400, UpdateOrganizationMembershipMetadataResponse404, UpdateOrganizationMembershipMetadataResponse422]]
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
    body: UpdateOrganizationMembershipMetadataBody,
) -> Optional[
    Union[
        UpdateOrganizationMembershipMetadataResponse200,
        UpdateOrganizationMembershipMetadataResponse400,
        UpdateOrganizationMembershipMetadataResponse404,
        UpdateOrganizationMembershipMetadataResponse422,
    ]
]:
    """Merge and update organization membership metadata

     Update an organization membership's metadata attributes by merging existing values with the provided
    parameters.
    Metadata values will be updated via a deep merge. Deep means that any nested JSON objects will be
    merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        user_id (str):
        body (UpdateOrganizationMembershipMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOrganizationMembershipMetadataResponse200, UpdateOrganizationMembershipMetadataResponse400, UpdateOrganizationMembershipMetadataResponse404, UpdateOrganizationMembershipMetadataResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
