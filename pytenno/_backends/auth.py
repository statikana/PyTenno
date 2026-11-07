"""Backend for Warframe.market authentication endpoints."""

from typing import Optional
from urllib.parse import quote_plus

from aiohttp import ClientResponse

from ..models.users import CurrentUser
from .core import RequestBackend


class AuthBackend(RequestBackend):
    """Backend methods for authentication (`signin`, `signout`, `restore`)."""

    async def _login(
        self,
        email: str,
        password: str,
        device_id: Optional[str] = None,
    ) -> CurrentUser:
        response: ClientResponse = await self._post(
            "/auth/signin",
            api_version="v1",
            return_raw_response=True,
            headers={"Authorization": ""},
            email=quote_plus(email),
            password=quote_plus(password),
            auth_type="header",
            device_id=device_id,
        )
        auth_header = response.headers.get("Authorization") or response.headers.get(
            "authorization"
        )
        if auth_header:
            token = (
                auth_header[4:]
                if auth_header.upper().startswith("JWT ")
                or auth_header.upper().startswith("BEARER ")
                else auth_header
            ).strip()
            if token.lower().startswith("er "):
                token = token[3:].strip()
            self.core.set_token(token)

        payload = await response.json(content_type=None)
        user_data = (
            payload.get("data")
            or payload.get("payload", {}).get("user")
            or payload
        )
        return CurrentUser._from_data(user_data)

    async def _signout(self) -> None:
        await self._post("/auth/signout", api_version="v2")
        self.core.set_token(None)

    async def _restore(self, email: str) -> None:
        await self._post(
            "/auth/restore",
            api_version="v1",
            email=quote_plus(email),
        )
