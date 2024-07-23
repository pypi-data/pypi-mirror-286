from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_organization_body import UpdateOrganizationBody
from ...models.update_organization_response_200 import UpdateOrganizationResponse200
from ...models.update_organization_response_402 import UpdateOrganizationResponse402
from ...models.update_organization_response_404 import UpdateOrganizationResponse404
from ...models.update_organization_response_422 import UpdateOrganizationResponse422
from ...types import Response


def _get_kwargs(
    organization_id: str,
    *,
    body: UpdateOrganizationBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/organizations/{organization_id}",
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
        UpdateOrganizationResponse200,
        UpdateOrganizationResponse402,
        UpdateOrganizationResponse404,
        UpdateOrganizationResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateOrganizationResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = UpdateOrganizationResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateOrganizationResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateOrganizationResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateOrganizationResponse200,
        UpdateOrganizationResponse402,
        UpdateOrganizationResponse404,
        UpdateOrganizationResponse422,
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
    body: UpdateOrganizationBody,
) -> Response[
    Union[
        UpdateOrganizationResponse200,
        UpdateOrganizationResponse402,
        UpdateOrganizationResponse404,
        UpdateOrganizationResponse422,
    ]
]:
    """Update an organization

     Updates an existing organization

    Args:
        organization_id (str):
        body (UpdateOrganizationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOrganizationResponse200, UpdateOrganizationResponse402, UpdateOrganizationResponse404, UpdateOrganizationResponse422]]
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
    body: UpdateOrganizationBody,
) -> Optional[
    Union[
        UpdateOrganizationResponse200,
        UpdateOrganizationResponse402,
        UpdateOrganizationResponse404,
        UpdateOrganizationResponse422,
    ]
]:
    """Update an organization

     Updates an existing organization

    Args:
        organization_id (str):
        body (UpdateOrganizationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOrganizationResponse200, UpdateOrganizationResponse402, UpdateOrganizationResponse404, UpdateOrganizationResponse422]
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
    body: UpdateOrganizationBody,
) -> Response[
    Union[
        UpdateOrganizationResponse200,
        UpdateOrganizationResponse402,
        UpdateOrganizationResponse404,
        UpdateOrganizationResponse422,
    ]
]:
    """Update an organization

     Updates an existing organization

    Args:
        organization_id (str):
        body (UpdateOrganizationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateOrganizationResponse200, UpdateOrganizationResponse402, UpdateOrganizationResponse404, UpdateOrganizationResponse422]]
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
    body: UpdateOrganizationBody,
) -> Optional[
    Union[
        UpdateOrganizationResponse200,
        UpdateOrganizationResponse402,
        UpdateOrganizationResponse404,
        UpdateOrganizationResponse422,
    ]
]:
    """Update an organization

     Updates an existing organization

    Args:
        organization_id (str):
        body (UpdateOrganizationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateOrganizationResponse200, UpdateOrganizationResponse402, UpdateOrganizationResponse404, UpdateOrganizationResponse422]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
            body=body,
        )
    ).parsed
