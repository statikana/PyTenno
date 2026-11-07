"""Backend for miscellaneous Warframe.market v2 endpoints."""

from typing import Optional

from ..models.locations import Location
from ..models.missions import DashboardShowcase, Mission, Npc, Versions
from ..models.users import Achievement
from .core import RequestBackend


class MiscBackend(RequestBackend):
    """Backend methods for `/v2/versions`, `/v2/locations`, `/v2/missions`, `/v2/npcs`, `/v2/achievements`, and `/v2/dashboard/showcase`."""

    async def _get_versions(self) -> Versions:
        data = await self._get("/versions")
        return Versions._from_data(data)

    async def _get_locations(self) -> list[Location]:
        data = await self._get("/locations")
        return [Location._from_data(loc) for loc in data]

    async def _get_missions(self) -> list[Mission]:
        data = await self._get("/missions")
        return [Mission._from_data(mission) for mission in data]

    async def _get_npcs(self) -> list[Npc]:
        data = await self._get("/npcs")
        return [Npc._from_data(npc) for npc in data]

    async def _get_achievements(self) -> list[Achievement]:
        data = await self._get("/achievements")
        return [Achievement._from_data(ach) for ach in data]

    async def _get_user_achievements(
        self,
        slug: str,
        featured: Optional[bool] = None,
    ) -> list[Achievement]:
        params = {"featured": featured} if featured is not None else None
        data = await self._get(f"/achievements/user/{slug}", params=params)
        return [Achievement._from_data(ach) for ach in data]

    async def _get_user_achievements_by_id(
        self,
        user_id: str,
        featured: Optional[bool] = None,
    ) -> list[Achievement]:
        params = {"featured": featured} if featured is not None else None
        data = await self._get(f"/achievements/userId/{user_id}", params=params)
        return [Achievement._from_data(ach) for ach in data]

    async def _get_dashboard_showcase(self) -> DashboardShowcase:
        data = await self._get("/dashboard/showcase")
        return DashboardShowcase._from_data(data)
