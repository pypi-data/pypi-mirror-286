from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_template_list_response_200_item import GetTemplateListResponse200Item
from ...models.get_template_list_response_400 import GetTemplateListResponse400
from ...models.get_template_list_response_401 import GetTemplateListResponse401
from ...models.get_template_list_response_422 import GetTemplateListResponse422
from ...models.get_template_list_template_type import GetTemplateListTemplateType
from ...types import Response


def _get_kwargs(
    template_type: GetTemplateListTemplateType,
) -> Dict[str, Any]:
    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/templates/{template_type}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetTemplateListResponse400,
        GetTemplateListResponse401,
        GetTemplateListResponse422,
        List["GetTemplateListResponse200Item"],
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetTemplateListResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = GetTemplateListResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = GetTemplateListResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = GetTemplateListResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        GetTemplateListResponse400,
        GetTemplateListResponse401,
        GetTemplateListResponse422,
        List["GetTemplateListResponse200Item"],
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_type: GetTemplateListTemplateType,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetTemplateListResponse400,
        GetTemplateListResponse401,
        GetTemplateListResponse422,
        List["GetTemplateListResponse200Item"],
    ]
]:
    """List all templates

     Returns a list of all templates.
    The templates are returned sorted by position.

    Args:
        template_type (GetTemplateListTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetTemplateListResponse400, GetTemplateListResponse401, GetTemplateListResponse422, List['GetTemplateListResponse200Item']]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_type: GetTemplateListTemplateType,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetTemplateListResponse400,
        GetTemplateListResponse401,
        GetTemplateListResponse422,
        List["GetTemplateListResponse200Item"],
    ]
]:
    """List all templates

     Returns a list of all templates.
    The templates are returned sorted by position.

    Args:
        template_type (GetTemplateListTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetTemplateListResponse400, GetTemplateListResponse401, GetTemplateListResponse422, List['GetTemplateListResponse200Item']]
    """

    return sync_detailed(
        template_type=template_type,
        client=client,
    ).parsed


async def asyncio_detailed(
    template_type: GetTemplateListTemplateType,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        GetTemplateListResponse400,
        GetTemplateListResponse401,
        GetTemplateListResponse422,
        List["GetTemplateListResponse200Item"],
    ]
]:
    """List all templates

     Returns a list of all templates.
    The templates are returned sorted by position.

    Args:
        template_type (GetTemplateListTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetTemplateListResponse400, GetTemplateListResponse401, GetTemplateListResponse422, List['GetTemplateListResponse200Item']]]
    """

    kwargs = _get_kwargs(
        template_type=template_type,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_type: GetTemplateListTemplateType,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        GetTemplateListResponse400,
        GetTemplateListResponse401,
        GetTemplateListResponse422,
        List["GetTemplateListResponse200Item"],
    ]
]:
    """List all templates

     Returns a list of all templates.
    The templates are returned sorted by position.

    Args:
        template_type (GetTemplateListTemplateType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetTemplateListResponse400, GetTemplateListResponse401, GetTemplateListResponse422, List['GetTemplateListResponse200Item']]
    """

    return (
        await asyncio_detailed(
            template_type=template_type,
            client=client,
        )
    ).parsed
