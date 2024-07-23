from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_template_response_200 import GetTemplateResponse200
from ...models.get_template_response_400 import GetTemplateResponse400
from ...models.get_template_response_401 import GetTemplateResponse401
from ...models.get_template_response_404 import GetTemplateResponse404
from ...models.get_template_template_type import GetTemplateTemplateType
from ...types import Response


def _get_kwargs(
    template_type: GetTemplateTemplateType,
    slug: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/templates/{template_type}/{slug}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetTemplateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetTemplateResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = GetTemplateResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_type: GetTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]:
    """Retrieve a template

     Returns the details of a template

    Args:
        template_type (GetTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        slug=slug,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_type: GetTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]:
    """Retrieve a template

     Returns the details of a template

    Args:
        template_type (GetTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]
    """

    return sync_detailed(
        template_type=template_type,
        slug=slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    template_type: GetTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]:
    """Retrieve a template

     Returns the details of a template

    Args:
        template_type (GetTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        slug=slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_type: GetTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]]:
    """Retrieve a template

     Returns the details of a template

    Args:
        template_type (GetTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetTemplateResponse200, GetTemplateResponse400, GetTemplateResponse401, GetTemplateResponse404]
    """

    return (
        await asyncio_detailed(
            template_type=template_type,
            slug=slug,
            client=client,
        )
    ).parsed
