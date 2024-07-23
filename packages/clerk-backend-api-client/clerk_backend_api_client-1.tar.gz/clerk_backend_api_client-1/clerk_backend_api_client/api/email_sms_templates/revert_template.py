from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.revert_template_response_200 import RevertTemplateResponse200
from ...models.revert_template_response_400 import RevertTemplateResponse400
from ...models.revert_template_response_401 import RevertTemplateResponse401
from ...models.revert_template_response_402 import RevertTemplateResponse402
from ...models.revert_template_response_404 import RevertTemplateResponse404
from ...models.revert_template_template_type import RevertTemplateTemplateType
from ...types import Response


def _get_kwargs(
    template_type: RevertTemplateTemplateType,
    slug: str,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/templates/{template_type}/{slug}/revert",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        RevertTemplateResponse200,
        RevertTemplateResponse400,
        RevertTemplateResponse401,
        RevertTemplateResponse402,
        RevertTemplateResponse404,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RevertTemplateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = RevertTemplateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = RevertTemplateResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = RevertTemplateResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = RevertTemplateResponse404.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        RevertTemplateResponse200,
        RevertTemplateResponse400,
        RevertTemplateResponse401,
        RevertTemplateResponse402,
        RevertTemplateResponse404,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_type: RevertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        RevertTemplateResponse200,
        RevertTemplateResponse400,
        RevertTemplateResponse401,
        RevertTemplateResponse402,
        RevertTemplateResponse404,
    ]
]:
    """Revert a template

     Reverts an updated template to its default state

    Args:
        template_type (RevertTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevertTemplateResponse200, RevertTemplateResponse400, RevertTemplateResponse401, RevertTemplateResponse402, RevertTemplateResponse404]]
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
    template_type: RevertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        RevertTemplateResponse200,
        RevertTemplateResponse400,
        RevertTemplateResponse401,
        RevertTemplateResponse402,
        RevertTemplateResponse404,
    ]
]:
    """Revert a template

     Reverts an updated template to its default state

    Args:
        template_type (RevertTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevertTemplateResponse200, RevertTemplateResponse400, RevertTemplateResponse401, RevertTemplateResponse402, RevertTemplateResponse404]
    """

    return sync_detailed(
        template_type=template_type,
        slug=slug,
        client=client,
    ).parsed


async def asyncio_detailed(
    template_type: RevertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        RevertTemplateResponse200,
        RevertTemplateResponse400,
        RevertTemplateResponse401,
        RevertTemplateResponse402,
        RevertTemplateResponse404,
    ]
]:
    """Revert a template

     Reverts an updated template to its default state

    Args:
        template_type (RevertTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[RevertTemplateResponse200, RevertTemplateResponse400, RevertTemplateResponse401, RevertTemplateResponse402, RevertTemplateResponse404]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
        slug=slug,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_type: RevertTemplateTemplateType,
    slug: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        RevertTemplateResponse200,
        RevertTemplateResponse400,
        RevertTemplateResponse401,
        RevertTemplateResponse402,
        RevertTemplateResponse404,
    ]
]:
    """Revert a template

     Reverts an updated template to its default state

    Args:
        template_type (RevertTemplateTemplateType):
        slug (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[RevertTemplateResponse200, RevertTemplateResponse400, RevertTemplateResponse401, RevertTemplateResponse402, RevertTemplateResponse404]
    """

    return (
        await asyncio_detailed(
            template_type=template_type,
            slug=slug,
            client=client,
        )
    ).parsed
