from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.upload_organization_logo_body import UploadOrganizationLogoBody
from ...models.upload_organization_logo_response_200 import UploadOrganizationLogoResponse200
from ...models.upload_organization_logo_response_400 import UploadOrganizationLogoResponse400
from ...models.upload_organization_logo_response_403 import UploadOrganizationLogoResponse403
from ...models.upload_organization_logo_response_404 import UploadOrganizationLogoResponse404
from ...models.upload_organization_logo_response_413 import UploadOrganizationLogoResponse413
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    body: UploadOrganizationLogoBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/organizations/{organization_id}/logo",
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        UploadOrganizationLogoResponse200,
        UploadOrganizationLogoResponse400,
        UploadOrganizationLogoResponse403,
        UploadOrganizationLogoResponse404,
        UploadOrganizationLogoResponse413,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UploadOrganizationLogoResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UploadOrganizationLogoResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UploadOrganizationLogoResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UploadOrganizationLogoResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE:
        response_413 = UploadOrganizationLogoResponse413.from_dict(response.json())

        return response_413
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UploadOrganizationLogoResponse200,
        UploadOrganizationLogoResponse400,
        UploadOrganizationLogoResponse403,
        UploadOrganizationLogoResponse404,
        UploadOrganizationLogoResponse413,
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
    body: UploadOrganizationLogoBody,
) -> Response[
    Union[
        UploadOrganizationLogoResponse200,
        UploadOrganizationLogoResponse400,
        UploadOrganizationLogoResponse403,
        UploadOrganizationLogoResponse404,
        UploadOrganizationLogoResponse413,
    ]
]:
    """Upload a logo for the organization

     Set or replace an organization's logo, by uploading an image file.
    This endpoint uses the `multipart/form-data` request content type and accepts a file of image type.
    The file size cannot exceed 10MB.
    Only the following file content types are supported: `image/jpeg`, `image/png`, `image/gif`,
    `image/webp`, `image/x-icon`, `image/vnd.microsoft.icon`.

    Args:
        organization_id (str):
        body (UploadOrganizationLogoBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UploadOrganizationLogoResponse200, UploadOrganizationLogoResponse400, UploadOrganizationLogoResponse403, UploadOrganizationLogoResponse404, UploadOrganizationLogoResponse413]]
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
    body: UploadOrganizationLogoBody,
) -> Optional[
    Union[
        UploadOrganizationLogoResponse200,
        UploadOrganizationLogoResponse400,
        UploadOrganizationLogoResponse403,
        UploadOrganizationLogoResponse404,
        UploadOrganizationLogoResponse413,
    ]
]:
    """Upload a logo for the organization

     Set or replace an organization's logo, by uploading an image file.
    This endpoint uses the `multipart/form-data` request content type and accepts a file of image type.
    The file size cannot exceed 10MB.
    Only the following file content types are supported: `image/jpeg`, `image/png`, `image/gif`,
    `image/webp`, `image/x-icon`, `image/vnd.microsoft.icon`.

    Args:
        organization_id (str):
        body (UploadOrganizationLogoBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UploadOrganizationLogoResponse200, UploadOrganizationLogoResponse400, UploadOrganizationLogoResponse403, UploadOrganizationLogoResponse404, UploadOrganizationLogoResponse413]
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
    body: UploadOrganizationLogoBody,
) -> Response[
    Union[
        UploadOrganizationLogoResponse200,
        UploadOrganizationLogoResponse400,
        UploadOrganizationLogoResponse403,
        UploadOrganizationLogoResponse404,
        UploadOrganizationLogoResponse413,
    ]
]:
    """Upload a logo for the organization

     Set or replace an organization's logo, by uploading an image file.
    This endpoint uses the `multipart/form-data` request content type and accepts a file of image type.
    The file size cannot exceed 10MB.
    Only the following file content types are supported: `image/jpeg`, `image/png`, `image/gif`,
    `image/webp`, `image/x-icon`, `image/vnd.microsoft.icon`.

    Args:
        organization_id (str):
        body (UploadOrganizationLogoBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UploadOrganizationLogoResponse200, UploadOrganizationLogoResponse400, UploadOrganizationLogoResponse403, UploadOrganizationLogoResponse404, UploadOrganizationLogoResponse413]]
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
    body: UploadOrganizationLogoBody,
) -> Optional[
    Union[
        UploadOrganizationLogoResponse200,
        UploadOrganizationLogoResponse400,
        UploadOrganizationLogoResponse403,
        UploadOrganizationLogoResponse404,
        UploadOrganizationLogoResponse413,
    ]
]:
    """Upload a logo for the organization

     Set or replace an organization's logo, by uploading an image file.
    This endpoint uses the `multipart/form-data` request content type and accepts a file of image type.
    The file size cannot exceed 10MB.
    Only the following file content types are supported: `image/jpeg`, `image/png`, `image/gif`,
    `image/webp`, `image/x-icon`, `image/vnd.microsoft.icon`.

    Args:
        organization_id (str):
        body (UploadOrganizationLogoBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UploadOrganizationLogoResponse200, UploadOrganizationLogoResponse400, UploadOrganizationLogoResponse403, UploadOrganizationLogoResponse404, UploadOrganizationLogoResponse413]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
