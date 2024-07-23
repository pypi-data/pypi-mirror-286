from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_user_metadata_body import UpdateUserMetadataBody
from ...models.update_user_metadata_response_200 import UpdateUserMetadataResponse200
from ...models.update_user_metadata_response_400 import UpdateUserMetadataResponse400
from ...models.update_user_metadata_response_401 import UpdateUserMetadataResponse401
from ...models.update_user_metadata_response_404 import UpdateUserMetadataResponse404
from ...models.update_user_metadata_response_422 import UpdateUserMetadataResponse422
from ...types import Response


def _get_kwargs(
    user_id: str,
    *,
    body: UpdateUserMetadataBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "patch",
        "url": f"/users/{user_id}/metadata",
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
        UpdateUserMetadataResponse200,
        UpdateUserMetadataResponse400,
        UpdateUserMetadataResponse401,
        UpdateUserMetadataResponse404,
        UpdateUserMetadataResponse422,
    ]
]:
    if response.status_code == HTTPStatus.OK:
        response_200 = UpdateUserMetadataResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = UpdateUserMetadataResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = UpdateUserMetadataResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = UpdateUserMetadataResponse404.from_dict(response.json())

        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = UpdateUserMetadataResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        UpdateUserMetadataResponse200,
        UpdateUserMetadataResponse400,
        UpdateUserMetadataResponse401,
        UpdateUserMetadataResponse404,
        UpdateUserMetadataResponse422,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateUserMetadataBody,
) -> Response[
    Union[
        UpdateUserMetadataResponse200,
        UpdateUserMetadataResponse400,
        UpdateUserMetadataResponse401,
        UpdateUserMetadataResponse404,
        UpdateUserMetadataResponse422,
    ]
]:
    """Merge and update a user's metadata

     Update a user's metadata attributes by merging existing values with the provided parameters.

    This endpoint behaves differently than the *Update a user* endpoint.
    Metadata values will not be replaced entirely.
    Instead, a deep merge will be performed.
    Deep means that any nested JSON objects will be merged as well.

    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        user_id (str):
        body (UpdateUserMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateUserMetadataResponse200, UpdateUserMetadataResponse400, UpdateUserMetadataResponse401, UpdateUserMetadataResponse404, UpdateUserMetadataResponse422]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateUserMetadataBody,
) -> Optional[
    Union[
        UpdateUserMetadataResponse200,
        UpdateUserMetadataResponse400,
        UpdateUserMetadataResponse401,
        UpdateUserMetadataResponse404,
        UpdateUserMetadataResponse422,
    ]
]:
    """Merge and update a user's metadata

     Update a user's metadata attributes by merging existing values with the provided parameters.

    This endpoint behaves differently than the *Update a user* endpoint.
    Metadata values will not be replaced entirely.
    Instead, a deep merge will be performed.
    Deep means that any nested JSON objects will be merged as well.

    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        user_id (str):
        body (UpdateUserMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateUserMetadataResponse200, UpdateUserMetadataResponse400, UpdateUserMetadataResponse401, UpdateUserMetadataResponse404, UpdateUserMetadataResponse422]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateUserMetadataBody,
) -> Response[
    Union[
        UpdateUserMetadataResponse200,
        UpdateUserMetadataResponse400,
        UpdateUserMetadataResponse401,
        UpdateUserMetadataResponse404,
        UpdateUserMetadataResponse422,
    ]
]:
    """Merge and update a user's metadata

     Update a user's metadata attributes by merging existing values with the provided parameters.

    This endpoint behaves differently than the *Update a user* endpoint.
    Metadata values will not be replaced entirely.
    Instead, a deep merge will be performed.
    Deep means that any nested JSON objects will be merged as well.

    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        user_id (str):
        body (UpdateUserMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[UpdateUserMetadataResponse200, UpdateUserMetadataResponse400, UpdateUserMetadataResponse401, UpdateUserMetadataResponse404, UpdateUserMetadataResponse422]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateUserMetadataBody,
) -> Optional[
    Union[
        UpdateUserMetadataResponse200,
        UpdateUserMetadataResponse400,
        UpdateUserMetadataResponse401,
        UpdateUserMetadataResponse404,
        UpdateUserMetadataResponse422,
    ]
]:
    """Merge and update a user's metadata

     Update a user's metadata attributes by merging existing values with the provided parameters.

    This endpoint behaves differently than the *Update a user* endpoint.
    Metadata values will not be replaced entirely.
    Instead, a deep merge will be performed.
    Deep means that any nested JSON objects will be merged as well.

    You can remove metadata keys at any level by setting their value to `null`.

    Args:
        user_id (str):
        body (UpdateUserMetadataBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[UpdateUserMetadataResponse200, UpdateUserMetadataResponse400, UpdateUserMetadataResponse401, UpdateUserMetadataResponse404, UpdateUserMetadataResponse422]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
