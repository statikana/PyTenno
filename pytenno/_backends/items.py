"""Backend for Warframe.market v2 item endpoints."""

from typing import Any, Optional

from ..models.enums import Platform, Subtype
from ..models.items import Item, ItemSet, ItemShort
from ..models.orders import OrderWithUser, TopOrders
from .core import RequestBackend


class ItemsBackend(RequestBackend):
    """Backend methods for `/v2/items`, `/v2/item/{slug}`, and `/v2/orders/item/{slug}`."""

    async def _get_all(self) -> list[ItemShort]:
        data = await self._get("/items")
        return [ItemShort._from_data(item) for item in data]

    async def _get_item(self, slug: str) -> Item:
        data = await self._get(f"/item/{slug}")
        return Item._from_data(data)

    async def _get_item_set(self, slug: str) -> ItemSet:
        data = await self._get(f"/item/{slug}/set")
        return ItemSet._from_data(data)

    async def _get_orders(
        self,
        slug: str,
        platform: Optional[Platform | str] = None,
    ) -> list[OrderWithUser]:
        headers: Optional[dict[str, str]] = None
        if platform is not None:
            plat_str = platform.value if isinstance(platform, Platform) else str(platform)
            headers = {"Platform": plat_str}
        data = await self._get(f"/orders/item/{slug}", headers=headers)
        return [OrderWithUser._from_data(order) for order in data]

    async def _get_top_orders(
        self,
        slug: str,
        *,
        platform: Optional[Platform | str] = None,
        rank: Optional[int] = None,
        rank_lt: Optional[int] = None,
        charges: Optional[int] = None,
        charges_lt: Optional[int] = None,
        amber_stars: Optional[int] = None,
        amber_stars_lt: Optional[int] = None,
        cyan_stars: Optional[int] = None,
        cyan_stars_lt: Optional[int] = None,
        subtype: Optional[Subtype | str] = None,
    ) -> TopOrders:
        headers: Optional[dict[str, str]] = None
        if platform is not None:
            plat_str = platform.value if isinstance(platform, Platform) else str(platform)
            headers = {"Platform": plat_str}
        subtype_val = subtype.value if isinstance(subtype, Subtype) else subtype
        params: dict[str, Any] = {
            "rank": rank,
            "rankLt": rank_lt,
            "charges": charges,
            "chargesLt": charges_lt,
            "amberStars": amber_stars,
            "amberStarsLt": amber_stars_lt,
            "cyanStars": cyan_stars,
            "cyanStarsLt": cyan_stars_lt,
            "subtype": subtype_val,
        }
        data = await self._get(
            f"/orders/item/{slug}/top",
            params=params,
            headers=headers,
        )
        return TopOrders._from_data(data)
