from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_instance_restrictions_body import UpdateInstanceRestrictionsBody
from ...models.update_instance_restrictions_response_200 import UpdateInstanceRestrictionsResponse200
from ...models.update_instance_restrictions_response_402 import UpdateInstanceRestrictionsResponse402
from ...models.update_instance_restrictions_response_422 import UpdateInstanceRestrictionsResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: UpdateInstanceRestrictionsBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": "/instance/restrictions",
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
        UpdateInstanceRestrictionsResponse200,
        UpdateInstanceRestrictionsResponse402,
        UpdateInstanceRestrictionsResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateInstanceRestrictionsResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = UpdateInstanceRestrictionsResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateInstanceRestrictionsResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateInstanceRestrictionsResponse200,
        UpdateInstanceRestrictionsResponse402,
        UpdateInstanceRestrictionsResponse422,
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
    body: UpdateInstanceRestrictionsBody,
) -> Response[
    Union[
        UpdateInstanceRestrictionsResponse200,
        UpdateInstanceRestrictionsResponse402,
        UpdateInstanceRestrictionsResponse422,
    ]
]:
    """Update instance restrictions

     Updates the restriction settings of an instance

    Args:
        body (UpdateInstanceRestrictionsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateInstanceRestrictionsResponse200, UpdateInstanceRestrictionsResponse402, UpdateInstanceRestrictionsResponse422]]
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
    body: UpdateInstanceRestrictionsBody,
) -> Optional[
    Union[
        UpdateInstanceRestrictionsResponse200,
        UpdateInstanceRestrictionsResponse402,
        UpdateInstanceRestrictionsResponse422,
    ]
]:
    """Update instance restrictions

     Updates the restriction settings of an instance

    Args:
        body (UpdateInstanceRestrictionsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateInstanceRestrictionsResponse200, UpdateInstanceRestrictionsResponse402, UpdateInstanceRestrictionsResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInstanceRestrictionsBody,
) -> Response[
    Union[
        UpdateInstanceRestrictionsResponse200,
        UpdateInstanceRestrictionsResponse402,
        UpdateInstanceRestrictionsResponse422,
    ]
]:
    """Update instance restrictions

     Updates the restriction settings of an instance

    Args:
        body (UpdateInstanceRestrictionsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateInstanceRestrictionsResponse200, UpdateInstanceRestrictionsResponse402, UpdateInstanceRestrictionsResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateInstanceRestrictionsBody,
) -> Optional[
    Union[
        UpdateInstanceRestrictionsResponse200,
        UpdateInstanceRestrictionsResponse402,
        UpdateInstanceRestrictionsResponse422,
    ]
]:
    """Update instance restrictions

     Updates the restriction settings of an instance

    Args:
        body (UpdateInstanceRestrictionsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateInstanceRestrictionsResponse200, UpdateInstanceRestrictionsResponse402, UpdateInstanceRestrictionsResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
