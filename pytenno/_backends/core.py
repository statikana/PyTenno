"""Core HTTP request backend for PyTenno."""

from typing import Any, Literal, Optional, TypeVar
from urllib.parse import urlencode

from aiohttp import ClientResponse

from ..constants import API_ROOT, V1_API_ROOT
from ..errors import (
    InvalidResponseError,
    NotFoundError,
    RateLimitError,
    UnauthorizedError,
)

T = TypeVar("T")


class RequestBackend:
    """Base backend that executes HTTP requests against the Warframe.market API."""

    def __init__(self, core: Any) -> None:
        self.core = core

    def _build_url(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        api_version: Literal["v1", "v2"] = "v2",
    ) -> str:
        root = API_ROOT if api_version == "v2" else V1_API_ROOT
        clean_ep = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        url = f"{root}{clean_ep}"
        if params:
            filtered = {
                k: ("true" if v is True else "false" if v is False else v)
                for k, v in params.items()
                if v is not None
            }
            if filtered:
                url = f"{url}?{urlencode(filtered)}"
        return url

    async def _unwrap_response(
        self,
        response: ClientResponse,
        return_raw_response: bool = False,
    ) -> Any:
        status = response.status
        if status == 429:
            raise RateLimitError(
                "Warframe.market rate limit exceeded (HTTP 429)",
                status_code=429,
            )

        if status == 204:
            return response if return_raw_response else None

        try:
            payload = await response.json(content_type=None)
        except Exception:
            text = await response.text()
            if status in (401, 403):
                raise UnauthorizedError(
                    f"Unauthorized request (HTTP {status}): {text[:200]}",
                    status_code=status,
                )
            if status == 404:
                raise NotFoundError(
                    f"Endpoint or resource not found (HTTP 404): {response.url}",
                    status_code=404,
                )
            raise InvalidResponseError(
                f"Unexpected non-JSON response (HTTP {status}): {text[:200]}",
                status_code=status,
            )

        api_error = payload.get("error") if isinstance(payload, dict) else None
        if status not in (200, 201) or api_error is not None:
            msg = f"Warframe.market API error (HTTP {status}): {api_error or payload}"
            if status in (401, 403):
                raise UnauthorizedError(msg, status_code=status, api_error=api_error)
            if status == 404:
                raise NotFoundError(msg, status_code=status, api_error=api_error)
            raise InvalidResponseError(msg, status_code=status, api_error=api_error)

        if return_raw_response:
            return response

        if isinstance(payload, dict):
            if "data" in payload:
                return payload["data"]
            if "payload" in payload:
                return payload["payload"]
        return payload

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        api_version: Literal["v1", "v2"] = "v2",
        return_raw_response: bool = False,
    ) -> Any:
        url = self._build_url(endpoint, params=params, api_version=api_version)
        req_headers = dict(headers) if headers else None
        async with self.core.session.request(
            method,
            url,
            json=json_body,
            headers=req_headers,
        ) as response:
            return await self._unwrap_response(
                response,
                return_raw_response=return_raw_response,
            )

    async def _get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        return_raw_response: bool = False,
        headers: Optional[dict[str, str]] = None,
        api_version: Literal["v1", "v2"] = "v2",
    ) -> Any:
        return await self._request(
            "GET",
            endpoint,
            params=params,
            headers=headers,
            api_version=api_version,
            return_raw_response=return_raw_response,
        )

    async def _post(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        return_raw_response: bool = False,
        headers: Optional[dict[str, str]] = None,
        api_version: Literal["v1", "v2"] = "v2",
        **kwargs: Any,
    ) -> Any:
        return await self._request(
            "POST",
            endpoint,
            params=params,
            json_body=kwargs if kwargs else None,
            headers=headers,
            api_version=api_version,
            return_raw_response=return_raw_response,
        )

    async def _patch(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        return_raw_response: bool = False,
        headers: Optional[dict[str, str]] = None,
        api_version: Literal["v1", "v2"] = "v2",
        **kwargs: Any,
    ) -> Any:
        return await self._request(
            "PATCH",
            endpoint,
            params=params,
            json_body=kwargs if kwargs else None,
            headers=headers,
            api_version=api_version,
            return_raw_response=return_raw_response,
        )

    async def _put(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        return_raw_response: bool = False,
        headers: Optional[dict[str, str]] = None,
        api_version: Literal["v1", "v2"] = "v2",
        **kwargs: Any,
    ) -> Any:
        return await self._request(
            "PUT",
            endpoint,
            params=params,
            json_body=kwargs if kwargs else None,
            headers=headers,
            api_version=api_version,
            return_raw_response=return_raw_response,
        )

    async def _delete(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        return_raw_response: bool = False,
        headers: Optional[dict[str, str]] = None,
        api_version: Literal["v1", "v2"] = "v2",
    ) -> Any:
        return await self._request(
            "DELETE",
            endpoint,
            params=params,
            headers=headers,
            api_version=api_version,
            return_raw_response=return_raw_response,
        )
