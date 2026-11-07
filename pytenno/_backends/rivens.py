"""Backend for Warframe.market v2 Riven endpoints."""

from ..models.rivens import RivenAttribute, RivenItem
from .core import RequestBackend


class RivensBackend(RequestBackend):
    """Backend methods for `/v2/riven/weapons`, `/v2/riven/weapon/{slug}`, and `/v2/riven/attributes`."""

    async def _get_weapons(self) -> list[RivenItem]:
        data = await self._get("/riven/weapons")
        return [RivenItem._from_data(item) for item in data]

    async def _get_weapon(self, slug: str) -> RivenItem:
        data = await self._get(f"/riven/weapon/{slug}")
        return RivenItem._from_data(data)

    async def _get_attributes(self) -> list[RivenAttribute]:
        data = await self._get("/riven/attributes")
        return [RivenAttribute._from_data(attr) for attr in data]
