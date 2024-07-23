from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_instance_organization_settings_body import UpdateInstanceOrganizationSettingsBody
from ...models.update_instance_organization_settings_response_200 import UpdateInstanceOrganizationSettingsResponse200
from ...models.update_instance_organization_settings_response_402 import UpdateInstanceOrganizationSettingsResponse402
from ...models.update_instance_organization_settings_response_404 import UpdateInstanceOrganizationSettingsResponse404
from ...models.update_instance_organization_settings_response_422 import UpdateInstanceOrganizationSettingsResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: UpdateInstanceOrganizationSettingsBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": "/instance/organization_settings",
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
        UpdateInstanceOrganizationSettingsResponse200,
        UpdateInstanceOrganizationSettingsResponse402,
        UpdateInstanceOrganizationSettingsResponse404,
        UpdateInstanceOrganizationSettingsResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateInstanceOrganizationSettingsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = UpdateInstanceOrganizationSettingsResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateInstanceOrganizationSettingsResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateInstanceOrganizationSettingsResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateInstanceOrganizationSettingsResponse200,
        UpdateInstanceOrganizationSettingsResponse402,
        UpdateInstanceOrganizationSettingsResponse404,
        UpdateInstanceOrganizationSettingsResponse422,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInstanceOrganizationSettingsBody,
) -> Response[
    Union[
        UpdateInstanceOrganizationSettingsResponse200,
        UpdateInstanceOrganizationSettingsResponse402,
        UpdateInstanceOrganizationSettingsResponse404,
        UpdateInstanceOrganizationSettingsResponse422,
    ]
]:
    """Update instance organization settings

     Updates the organization settings of the instance

    Args:
        body (UpdateInstanceOrganizationSettingsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateInstanceOrganizationSettingsResponse200, UpdateInstanceOrganizationSettingsResponse402, UpdateInstanceOrganizationSettingsResponse404, UpdateInstanceOrganizationSettingsResponse422]]
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
    body: UpdateInstanceOrganizationSettingsBody,
) -> Optional[
    Union[
        UpdateInstanceOrganizationSettingsResponse200,
        UpdateInstanceOrganizationSettingsResponse402,
        UpdateInstanceOrganizationSettingsResponse404,
        UpdateInstanceOrganizationSettingsResponse422,
    ]
]:
    """Update instance organization settings

     Updates the organization settings of the instance

    Args:
        body (UpdateInstanceOrganizationSettingsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateInstanceOrganizationSettingsResponse200, UpdateInstanceOrganizationSettingsResponse402, UpdateInstanceOrganizationSettingsResponse404, UpdateInstanceOrganizationSettingsResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInstanceOrganizationSettingsBody,
) -> Response[
    Union[
        UpdateInstanceOrganizationSettingsResponse200,
        UpdateInstanceOrganizationSettingsResponse402,
        UpdateInstanceOrganizationSettingsResponse404,
        UpdateInstanceOrganizationSettingsResponse422,
    ]
]:
    """Update instance organization settings

     Updates the organization settings of the instance

    Args:
        body (UpdateInstanceOrganizationSettingsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateInstanceOrganizationSettingsResponse200, UpdateInstanceOrganizationSettingsResponse402, UpdateInstanceOrganizationSettingsResponse404, UpdateInstanceOrganizationSettingsResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInstanceOrganizationSettingsBody,
) -> Optional[
    Union[
        UpdateInstanceOrganizationSettingsResponse200,
        UpdateInstanceOrganizationSettingsResponse402,
        UpdateInstanceOrganizationSettingsResponse404,
        UpdateInstanceOrganizationSettingsResponse422,
    ]
]:
    """Update instance organization settings

     Updates the organization settings of the instance

    Args:
        body (UpdateInstanceOrganizationSettingsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateInstanceOrganizationSettingsResponse200, UpdateInstanceOrganizationSettingsResponse402, UpdateInstanceOrganizationSettingsResponse404, UpdateInstanceOrganizationSettingsResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
