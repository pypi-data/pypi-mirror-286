from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_saml_connection_body import UpdateSAMLConnectionBody
from ...models.update_saml_connection_response_200 import UpdateSAMLConnectionResponse200
from ...models.update_saml_connection_response_402 import UpdateSAMLConnectionResponse402
from ...models.update_saml_connection_response_403 import UpdateSAMLConnectionResponse403
from ...models.update_saml_connection_response_404 import UpdateSAMLConnectionResponse404
from ...models.update_saml_connection_response_422 import UpdateSAMLConnectionResponse422
from ...types import Response


def _get_kwargs(
    saml_connection_id: str,
    *,
    body: UpdateSAMLConnectionBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/saml_connections/{saml_connection_id}",
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
        UpdateSAMLConnectionResponse200,
        UpdateSAMLConnectionResponse402,
        UpdateSAMLConnectionResponse403,
        UpdateSAMLConnectionResponse404,
        UpdateSAMLConnectionResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateSAMLConnectionResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = UpdateSAMLConnectionResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = UpdateSAMLConnectionResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateSAMLConnectionResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateSAMLConnectionResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateSAMLConnectionResponse200,
        UpdateSAMLConnectionResponse402,
        UpdateSAMLConnectionResponse403,
        UpdateSAMLConnectionResponse404,
        UpdateSAMLConnectionResponse422,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSAMLConnectionBody,
) -> Response[
    Union[
        UpdateSAMLConnectionResponse200,
        UpdateSAMLConnectionResponse402,
        UpdateSAMLConnectionResponse403,
        UpdateSAMLConnectionResponse404,
        UpdateSAMLConnectionResponse422,
    ]
]:
    """Update a SAML Connection

     Updates the SAML Connection whose ID matches the provided `id` in the path.

    Args:
        saml_connection_id (str):
        body (UpdateSAMLConnectionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateSAMLConnectionResponse200, UpdateSAMLConnectionResponse402, UpdateSAMLConnectionResponse403, UpdateSAMLConnectionResponse404, UpdateSAMLConnectionResponse422]]
    """

    kwargs = _get_kwargs(
        saml_connection_id=saml_connection_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSAMLConnectionBody,
) -> Optional[
    Union[
        UpdateSAMLConnectionResponse200,
        UpdateSAMLConnectionResponse402,
        UpdateSAMLConnectionResponse403,
        UpdateSAMLConnectionResponse404,
        UpdateSAMLConnectionResponse422,
    ]
]:
    """Update a SAML Connection

     Updates the SAML Connection whose ID matches the provided `id` in the path.

    Args:
        saml_connection_id (str):
        body (UpdateSAMLConnectionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateSAMLConnectionResponse200, UpdateSAMLConnectionResponse402, UpdateSAMLConnectionResponse403, UpdateSAMLConnectionResponse404, UpdateSAMLConnectionResponse422]
    """

    return sync_detailed(
        saml_connection_id=saml_connection_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSAMLConnectionBody,
) -> Response[
    Union[
        UpdateSAMLConnectionResponse200,
        UpdateSAMLConnectionResponse402,
        UpdateSAMLConnectionResponse403,
        UpdateSAMLConnectionResponse404,
        UpdateSAMLConnectionResponse422,
    ]
]:
    """Update a SAML Connection

     Updates the SAML Connection whose ID matches the provided `id` in the path.

    Args:
        saml_connection_id (str):
        body (UpdateSAMLConnectionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateSAMLConnectionResponse200, UpdateSAMLConnectionResponse402, UpdateSAMLConnectionResponse403, UpdateSAMLConnectionResponse404, UpdateSAMLConnectionResponse422]]
    """

    kwargs = _get_kwargs(
        saml_connection_id=saml_connection_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    saml_connection_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateSAMLConnectionBody,
) -> Optional[
    Union[
        UpdateSAMLConnectionResponse200,
        UpdateSAMLConnectionResponse402,
        UpdateSAMLConnectionResponse403,
        UpdateSAMLConnectionResponse404,
        UpdateSAMLConnectionResponse422,
    ]
]:
    """Update a SAML Connection

     Updates the SAML Connection whose ID matches the provided `id` in the path.

    Args:
        saml_connection_id (str):
        body (UpdateSAMLConnectionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateSAMLConnectionResponse200, UpdateSAMLConnectionResponse402, UpdateSAMLConnectionResponse403, UpdateSAMLConnectionResponse404, UpdateSAMLConnectionResponse422]
    """

    return (
        await asyncio_detailed(
            saml_connection_id=saml_connection_id,
            client=client,
            body=body,
        )
    ).parsed
