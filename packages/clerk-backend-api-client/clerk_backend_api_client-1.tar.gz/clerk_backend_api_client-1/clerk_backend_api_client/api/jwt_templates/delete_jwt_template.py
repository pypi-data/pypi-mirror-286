from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_jwt_template_response_200 import DeleteJWTTemplateResponse200
from ...models.delete_jwt_template_response_403 import DeleteJWTTemplateResponse403
from ...models.delete_jwt_template_response_404 import DeleteJWTTemplateResponse404
from ...types import Response


def _get_kwargs(
    template_id: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": f"/jwt_templates/{template_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = DeleteJWTTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = DeleteJWTTemplateResponse403.from_dict(response.json())

        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = DeleteJWTTemplateResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]:
    """Delete a Template

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        template_id=template_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]:
    """Delete a Template

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]
    """

    return sync_detailed(
        template_id=template_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]:
    """Delete a Template

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        template_id=template_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]]:
    """Delete a Template

    Args:
        template_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteJWTTemplateResponse200, DeleteJWTTemplateResponse403, DeleteJWTTemplateResponse404]
    """

    return (
        await asyncio_detailed(
            template_id=template_id,
            client=client,
        )
    ).parsed
