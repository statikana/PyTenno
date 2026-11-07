"""Module holding the Rivens interface class."""

from .._backends.rivens import RivensBackend
from ..models.rivens import RivenAttribute, RivenItem


class Rivens(RivensBackend):
    """Interface for querying Warframe.market v2 Riven weapons and attributes."""

    async def get_weapons(self) -> list[RivenItem]:
        """Fetches all tradable Riven weapons (`GET /v2/riven/weapons`).

        Returns
        -------
        list[RivenItem]
            List of all Riven-compatible weapons and their dispositions.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     weapons = await tenno.rivens.get_weapons()
        ...     for weapon in weapons[:5]:
        ...         print(weapon.name, weapon.slug, weapon.disposition)
        """
        return await self._get_weapons()

    async def get_items(self) -> list[RivenItem]:
        """Backward-compatible alias for :meth:`get_weapons`."""
        return await self._get_weapons()

    async def get_weapon(self, slug: str) -> RivenItem:
        """Fetches a single Riven weapon by its slug (`GET /v2/riven/weapon/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the Riven weapon (e.g., ``"braton"``).

        Returns
        -------
        RivenItem

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     braton = await tenno.rivens.get_weapon("braton")
        ...     print(braton.name, braton.disposition, braton.riven_type)
        """
        return await self._get_weapon(slug)

    async def get_attributes(self) -> list[RivenAttribute]:
        """Fetches all Riven attributes (`GET /v2/riven/attributes`).

        Returns
        -------
        list[RivenAttribute]
            List of all Riven stat attributes, prefixes, suffixes, and units.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     attrs = await tenno.rivens.get_attributes()
        ...     for attr in attrs[:5]:
        ...         print(attr.name, attr.slug, attr.prefix, attr.suffix)
        """
        return await self._get_attributes()
