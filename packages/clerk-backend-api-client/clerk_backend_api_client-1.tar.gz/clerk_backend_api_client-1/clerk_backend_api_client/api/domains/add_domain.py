from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_domain_body import AddDomainBody
from ...models.add_domain_response_200 import AddDomainResponse200
from ...models.add_domain_response_400 import AddDomainResponse400
from ...models.add_domain_response_402 import AddDomainResponse402
from ...models.add_domain_response_422 import AddDomainResponse422
from ...types import Response


def _get_kwargs(
    *,
    body: AddDomainBody,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/domains",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AddDomainResponse200.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = AddDomainResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.PAYMENT_REQUIRED:
        response_402 = AddDomainResponse402.from_dict(response.json())

        return response_402
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = AddDomainResponse422.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddDomainBody,
) -> Response[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]:
    """Add a domain

     Add a new domain for your instance.
    Useful in the case of multi-domain instances, allows adding satellite domains to an instance.
    The new domain must have a `name`. The domain name can contain the port for development instances,
    like `localhost:3000`.
    At the moment, instances can have only one primary domain, so the `is_satellite` parameter must be
    set to `true`.
    If you're planning to configure the new satellite domain to run behind a proxy, pass the `proxy_url`
    parameter accordingly.

    Args:
        body (AddDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]
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
    body: AddDomainBody,
) -> Optional[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]:
    """Add a domain

     Add a new domain for your instance.
    Useful in the case of multi-domain instances, allows adding satellite domains to an instance.
    The new domain must have a `name`. The domain name can contain the port for development instances,
    like `localhost:3000`.
    At the moment, instances can have only one primary domain, so the `is_satellite` parameter must be
    set to `true`.
    If you're planning to configure the new satellite domain to run behind a proxy, pass the `proxy_url`
    parameter accordingly.

    Args:
        body (AddDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddDomainBody,
) -> Response[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]:
    """Add a domain

     Add a new domain for your instance.
    Useful in the case of multi-domain instances, allows adding satellite domains to an instance.
    The new domain must have a `name`. The domain name can contain the port for development instances,
    like `localhost:3000`.
    At the moment, instances can have only one primary domain, so the `is_satellite` parameter must be
    set to `true`.
    If you're planning to configure the new satellite domain to run behind a proxy, pass the `proxy_url`
    parameter accordingly.

    Args:
        body (AddDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: AddDomainBody,
) -> Optional[Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]]:
    """Add a domain

     Add a new domain for your instance.
    Useful in the case of multi-domain instances, allows adding satellite domains to an instance.
    The new domain must have a `name`. The domain name can contain the port for development instances,
    like `localhost:3000`.
    At the moment, instances can have only one primary domain, so the `is_satellite` parameter must be
    set to `true`.
    If you're planning to configure the new satellite domain to run behind a proxy, pass the `proxy_url`
    parameter accordingly.

    Args:
        body (AddDomainBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddDomainResponse200, AddDomainResponse400, AddDomainResponse402, AddDomainResponse422]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
