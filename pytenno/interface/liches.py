"""Module holding the Liches and Sisters interface classes."""

from .._backends.liches import LichesBackend, SistersBackend
from ..models.liches import (
    LichEphemera,
    LichQuirk,
    LichWeapon,
    SisterEphemera,
    SisterQuirk,
    SisterWeapon,
)


class Liches(LichesBackend):
    """Interface for querying Warframe.market v2 Kuva Lich weapons, ephemeras, and quirks."""

    async def get_weapons(self) -> list[LichWeapon]:
        """Fetches all tradable Kuva Lich weapons (`GET /v2/lich/weapons`).

        Returns
        -------
        list[LichWeapon]

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     weapons = await tenno.liches.get_weapons()
        ...     for weapon in weapons[:5]:
        ...         print(weapon.name, weapon.slug, weapon.req_mastery_rank)
        """
        return await self._get_weapons()

    async def get_weapon(self, slug: str) -> LichWeapon:
        """Fetches a single Kuva Lich weapon by its slug (`GET /v2/lich/weapon/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the Kuva weapon (e.g., ``"kuva_bramma"``).

        Returns
        -------
        LichWeapon
        """
        return await self._get_weapon(slug)

    async def get_ephemeras(self) -> list[LichEphemera]:
        """Fetches all Kuva Lich ephemeras (`GET /v2/lich/ephemeras`).

        Returns
        -------
        list[LichEphemera]
        """
        return await self._get_ephemeras()

    async def get_ephemera(self, slug: str) -> LichEphemera:
        """Fetches a single Kuva Lich ephemera by its slug (`GET /v2/lich/ephemera/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the ephemera (e.g., ``"vengeful_charge"``).

        Returns
        -------
        LichEphemera
        """
        return await self._get_ephemera(slug)

    async def get_quirks(self) -> list[LichQuirk]:
        """Fetches all Kuva Lich quirks (`GET /v2/lich/quirks`).

        Returns
        -------
        list[LichQuirk]
        """
        return await self._get_quirks()

    async def get_quirk(self, slug: str) -> LichQuirk:
        """Fetches a single Kuva Lich quirk by its slug (`GET /v2/lich/quirk/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the quirk (e.g., ``"poor_sense_of_balance"``).

        Returns
        -------
        LichQuirk
        """
        return await self._get_quirk(slug)


class Sisters(SistersBackend):
    """Interface for querying Warframe.market v2 Sister of Parvos weapons, ephemeras, and quirks."""

    async def get_weapons(self) -> list[SisterWeapon]:
        """Fetches all tradable Sister of Parvos weapons (`GET /v2/sister/weapons`).

        Returns
        -------
        list[SisterWeapon]

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     weapons = await tenno.sisters.get_weapons()
        ...     for weapon in weapons[:5]:
        ...         print(weapon.name, weapon.slug, weapon.req_mastery_rank)
        """
        return await self._get_weapons()

    async def get_weapon(self, slug: str) -> SisterWeapon:
        """Fetches a single Sister of Parvos weapon by its slug (`GET /v2/sister/weapon/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the Tenet weapon (e.g., ``"tenet_tetra"``).

        Returns
        -------
        SisterWeapon
        """
        return await self._get_weapon(slug)

    async def get_ephemeras(self) -> list[SisterEphemera]:
        """Fetches all Sister of Parvos ephemeras (`GET /v2/sister/ephemeras`).

        Returns
        -------
        list[SisterEphemera]
        """
        return await self._get_ephemeras()

    async def get_ephemera(self, slug: str) -> SisterEphemera:
        """Fetches a single Sister of Parvos ephemera by its slug (`GET /v2/sister/ephemera/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the ephemera (e.g., ``"gloriana_ephemera"``).

        Returns
        -------
        SisterEphemera
        """
        return await self._get_ephemera(slug)

    async def get_quirks(self) -> list[SisterQuirk]:
        """Fetches all Sister of Parvos quirks (`GET /v2/sister/quirks`).

        Returns
        -------
        list[SisterQuirk]
        """
        return await self._get_quirks()

    async def get_quirk(self, slug: str) -> SisterQuirk:
        """Fetches a single Sister of Parvos quirk by its slug (`GET /v2/sister/quirk/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the quirk (e.g., ``"coward"``).

        Returns
        -------
        SisterQuirk
        """
        return await self._get_quirk(slug)
