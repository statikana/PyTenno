"""Backend for Warframe.market v2 Kuva Lich and Sister of Parvos endpoints."""

from ..models.liches import (
    LichEphemera,
    LichQuirk,
    LichWeapon,
    SisterEphemera,
    SisterQuirk,
    SisterWeapon,
)
from .core import RequestBackend


class LichesBackend(RequestBackend):
    """Backend methods for `/v2/lich/...` and `/v2/sister/...` endpoints."""

    async def _get_weapons(self) -> list[LichWeapon]:
        data = await self._get("/lich/weapons")
        return [LichWeapon._from_data(weapon) for weapon in data]

    async def _get_weapon(self, slug: str) -> LichWeapon:
        data = await self._get(f"/lich/weapon/{slug}")
        return LichWeapon._from_data(data)

    async def _get_ephemeras(self) -> list[LichEphemera]:
        data = await self._get("/lich/ephemeras")
        return [LichEphemera._from_data(ephemera) for ephemera in data]

    async def _get_ephemera(self, slug: str) -> LichEphemera:
        data = await self._get(f"/lich/ephemera/{slug}")
        return LichEphemera._from_data(data)

    async def _get_quirks(self) -> list[LichQuirk]:
        data = await self._get("/lich/quirks")
        return [LichQuirk._from_data(quirk) for quirk in data]

    async def _get_quirk(self, slug: str) -> LichQuirk:
        data = await self._get(f"/lich/quirk/{slug}")
        return LichQuirk._from_data(data)


class SistersBackend(RequestBackend):
    """Backend methods for `/v2/sister/...` endpoints."""

    async def _get_weapons(self) -> list[SisterWeapon]:
        data = await self._get("/sister/weapons")
        return [SisterWeapon._from_data(weapon) for weapon in data]

    async def _get_weapon(self, slug: str) -> SisterWeapon:
        data = await self._get(f"/sister/weapon/{slug}")
        return SisterWeapon._from_data(data)

    async def _get_ephemeras(self) -> list[SisterEphemera]:
        data = await self._get("/sister/ephemeras")
        return [SisterEphemera._from_data(ephemera) for ephemera in data]

    async def _get_ephemera(self, slug: str) -> SisterEphemera:
        data = await self._get(f"/sister/ephemera/{slug}")
        return SisterEphemera._from_data(data)

    async def _get_quirks(self) -> list[SisterQuirk]:
        data = await self._get("/sister/quirks")
        return [SisterQuirk._from_data(quirk) for quirk in data]

    async def _get_quirk(self, slug: str) -> SisterQuirk:
        data = await self._get(f"/sister/quirk/{slug}")
        return SisterQuirk._from_data(data)
