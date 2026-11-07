"""Module holding the Misc interface class."""

from typing import Optional

from .._backends.misc import MiscBackend
from ..models.locations import Location
from ..models.missions import DashboardShowcase, Mission, Npc, Versions
from ..models.users import Achievement


class Misc(MiscBackend):
    """Interface for Warframe.market v2 manifest versions, locations, missions, NPCs, achievements, and showcase."""

    async def get_versions(self) -> Versions:
        """Fetches current server resource and manifest collection versions (`GET /v2/versions`).

        Returns
        -------
        Versions
            Object containing mobile app versions and collection hash strings.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     versions = await tenno.misc.get_versions()
        ...     print(versions.collections.items, versions.updated_at)
        """
        return await self._get_versions()

    async def get_locations(self) -> list[Location]:
        """Fetches all Warframe star chart locations (`GET /v2/locations`).

        Returns
        -------
        list[Location]

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     locations = await tenno.misc.get_locations()
        ...     for loc in locations[:5]:
        ...         print(loc.node_name, loc.system_name, loc.faction)
        """
        return await self._get_locations()

    async def get_missions(self) -> list[Mission]:
        """Fetches all Warframe missions (`GET /v2/missions`).

        Returns
        -------
        list[Mission]

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     missions = await tenno.misc.get_missions()
        ...     for mission in missions[:5]:
        ...         print(mission.name, mission.slug)
        """
        return await self._get_missions()

    async def get_npcs(self) -> list[Npc]:
        """Fetches all Warframe NPCs (`GET /v2/npcs`).

        Returns
        -------
        list[Npc]

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     npcs = await tenno.misc.get_npcs()
        ...     for npc in npcs[:5]:
        ...         print(npc.name, npc.slug)
        """
        return await self._get_npcs()

    async def get_achievements(self) -> list[Achievement]:
        """Fetches all non-secret Warframe.market achievements (`GET /v2/achievements`).

        Returns
        -------
        list[Achievement]
        """
        return await self._get_achievements()

    async def get_user_achievements(
        self,
        slug: str,
        *,
        featured: Optional[bool] = None,
    ) -> list[Achievement]:
        """Fetches achievements unlocked by a user via their slug (`GET /v2/achievements/user/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the user.
        featured : bool, optional
            If ``True``, returns only featured achievements.

        Returns
        -------
        list[Achievement]
        """
        return await self._get_user_achievements(slug, featured=featured)

    async def get_user_achievements_by_id(
        self,
        user_id: str,
        *,
        featured: Optional[bool] = None,
    ) -> list[Achievement]:
        """Fetches achievements unlocked by a user via their user ID (`GET /v2/achievements/userId/{user_id}`).

        Parameters
        ----------
        user_id : str
            The unique ID of the user.
        featured : bool, optional
            If ``True``, returns only featured achievements.

        Returns
        -------
        list[Achievement]
        """
        return await self._get_user_achievements_by_id(user_id, featured=featured)

    async def get_dashboard_showcase(self) -> DashboardShowcase:
        """Fetches the featured items showcase (`GET /v2/dashboard/showcase`).

        Returns
        -------
        DashboardShowcase
        """
        return await self._get_dashboard_showcase()
