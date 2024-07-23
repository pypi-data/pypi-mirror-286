from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.merge_organization_metadata_body import MergeOrganizationMetadataBody
from ...models.merge_organization_metadata_response_200 import MergeOrganizationMetadataResponse200
from ...models.merge_organization_metadata_response_400 import MergeOrganizationMetadataResponse400
from ...models.merge_organization_metadata_response_401 import MergeOrganizationMetadataResponse401
from ...models.merge_organization_metadata_response_404 import MergeOrganizationMetadataResponse404
from ...models.merge_organization_metadata_response_422 import MergeOrganizationMetadataResponse422
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    body: MergeOrganizationMetadataBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/organizations/{organization_id}/metadata",
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
        MergeOrganizationMetadataResponse200,
        MergeOrganizationMetadataResponse400,
        MergeOrganizationMetadataResponse401,
        MergeOrganizationMetadataResponse404,
        MergeOrganizationMetadataResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MergeOrganizationMetadataResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = MergeOrganizationMetadataResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = MergeOrganizationMetadataResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = MergeOrganizationMetadataResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = MergeOrganizationMetadataResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        MergeOrganizationMetadataResponse200,
        MergeOrganizationMetadataResponse400,
        MergeOrganizationMetadataResponse401,
        MergeOrganizationMetadataResponse404,
        MergeOrganizationMetadataResponse422,
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
    body: MergeOrganizationMetadataBody,
) -> Response[
    Union[
        MergeOrganizationMetadataResponse200,
        MergeOrganizationMetadataResponse400,
        MergeOrganizationMetadataResponse401,
        MergeOrganizationMetadataResponse404,
        MergeOrganizationMetadataResponse422,
    ]
]:
    """Merge and update metadata for an organization

     Update organization metadata attributes by merging existing values with the provided parameters.
    Metadata values will be updated via a deep merge.
    Deep meaning that any nested JSON objects will be merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        body (MergeOrganizationMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[MergeOrganizationMetadataResponse200, MergeOrganizationMetadataResponse400, MergeOrganizationMetadataResponse401, MergeOrganizationMetadataResponse404, MergeOrganizationMetadataResponse422]]
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
    body: MergeOrganizationMetadataBody,
) -> Optional[
    Union[
        MergeOrganizationMetadataResponse200,
        MergeOrganizationMetadataResponse400,
        MergeOrganizationMetadataResponse401,
        MergeOrganizationMetadataResponse404,
        MergeOrganizationMetadataResponse422,
    ]
]:
    """Merge and update metadata for an organization

     Update organization metadata attributes by merging existing values with the provided parameters.
    Metadata values will be updated via a deep merge.
    Deep meaning that any nested JSON objects will be merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        body (MergeOrganizationMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[MergeOrganizationMetadataResponse200, MergeOrganizationMetadataResponse400, MergeOrganizationMetadataResponse401, MergeOrganizationMetadataResponse404, MergeOrganizationMetadataResponse422]
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
    body: MergeOrganizationMetadataBody,
) -> Response[
    Union[
        MergeOrganizationMetadataResponse200,
        MergeOrganizationMetadataResponse400,
        MergeOrganizationMetadataResponse401,
        MergeOrganizationMetadataResponse404,
        MergeOrganizationMetadataResponse422,
    ]
]:
    """Merge and update metadata for an organization

     Update organization metadata attributes by merging existing values with the provided parameters.
    Metadata values will be updated via a deep merge.
    Deep meaning that any nested JSON objects will be merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        body (MergeOrganizationMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[MergeOrganizationMetadataResponse200, MergeOrganizationMetadataResponse400, MergeOrganizationMetadataResponse401, MergeOrganizationMetadataResponse404, MergeOrganizationMetadataResponse422]]
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
    body: MergeOrganizationMetadataBody,
) -> Optional[
    Union[
        MergeOrganizationMetadataResponse200,
        MergeOrganizationMetadataResponse400,
        MergeOrganizationMetadataResponse401,
        MergeOrganizationMetadataResponse404,
        MergeOrganizationMetadataResponse422,
    ]
]:
    """Merge and update metadata for an organization

     Update organization metadata attributes by merging existing values with the provided parameters.
    Metadata values will be updated via a deep merge.
    Deep meaning that any nested JSON objects will be merged as well.
    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        organization_id (str):
        body (MergeOrganizationMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[MergeOrganizationMetadataResponse200, MergeOrganizationMetadataResponse400, MergeOrganizationMetadataResponse401, MergeOrganizationMetadataResponse404, MergeOrganizationMetadataResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
