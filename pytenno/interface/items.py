"""Module holding the Items interface class."""

from typing import Optional

from .._backends.items import ItemsBackend
from ..models.enums import Platform, Subtype
from ..models.items import Item, ItemSet, ItemShort
from ..models.orders import OrderWithUser, TopOrders


class Items(ItemsBackend):
    """Interface for querying Warframe.market v2 items, sets, and item orders."""

    async def get_all(self) -> list[ItemShort]:
        """Fetches the list of all tradable items (`GET /v2/items`).

        Returns
        -------
        list[ItemShort]
            Compact representations of all tradable items on Warframe.market.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     items = await tenno.items.get_all()
        ...     for item in items[:5]:
        ...         print(item.name, item.slug, item.id)
        """
        return await self._get_all()

    async def get_item(self, url_name: str) -> Item:
        """Fetches full details for a single item by its slug (`GET /v2/item/{slug}`).

        Parameters
        ----------
        url_name : str
            The URL-friendly slug of the item (e.g., ``"nikana_prime_set"`` or ``"blind_rage"``).

        Returns
        -------
        Item
            The full item metadata including tags, trading tax, mastery rank, and localized ``i18n`` fields.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     item = await tenno.items.get_item("nikana_prime_set")
        ...     print(item.name, item.ducats, item.req_mastery_rank, item.trading_tax)
        """
        return await self._get_item(url_name)

    async def get_item_set(self, url_name: str) -> ItemSet:
        """Fetches all items belonging to an item's set (`GET /v2/item/{slug}/set`).

        Parameters
        ----------
        url_name : str
            The URL-friendly slug of the set or any part in the set (e.g., ``"nikana_prime_blueprint"``).

        Returns
        -------
        ItemSet
            The set container holding all :class:`Item` objects in the set.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     item_set = await tenno.items.get_item_set("nikana_prime_blueprint")
        ...     print("Root set:", item_set.root.name)
        ...     for part in item_set.items:
        ...         print(" -", part.name, part.slug)
        """
        return await self._get_item_set(url_name)

    async def get_orders(
        self,
        url_name: str,
        *,
        platform: Optional[Platform] = None,
    ) -> list[OrderWithUser]:
        """Fetches all active buy and sell orders for an item (`GET /v2/orders/item/{slug}`).

        Parameters
        ----------
        url_name : str
            The URL-friendly slug of the item (e.g., ``"nikana_prime_set"``).
        platform : Platform, optional
            Override the client's default platform for this request.

        Returns
        -------
        list[OrderWithUser]
            Active orders from users who were online within the last 7 days.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     orders = await tenno.items.get_orders("nikana_prime_set")
        ...     for order in orders[:5]:
        ...         print(order.user.ingame_name, order.type.value, order.platinum)
        """
        return await self._get_orders(url_name, platform=platform)

    async def get_top_orders(
        self,
        url_name: str,
        *,
        platform: Optional[Platform] = None,
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
        """Fetches the top 5 online buy and top 5 online sell orders for an item (`GET /v2/orders/item/{slug}/top`).

        Parameters
        ----------
        url_name : str
            The URL-friendly slug of the item (e.g., ``"blind_rage"``).
        platform : Platform, optional
            Override the client's default platform for this request.
        rank : int, optional
            Filter orders by exact mod/arcane rank.
        rank_lt : int, optional
            Filter orders with a rank strictly less than this value.
        charges : int, optional
            Filter orders by exact remaining charges (e.g., Requiem mods).
        charges_lt : int, optional
            Filter orders with remaining charges strictly less than this value.
        amber_stars : int, optional
            Filter Ayatan sculpture orders by exact Amber Stars count.
        amber_stars_lt : int, optional
            Filter Ayatan sculpture orders with Amber Stars strictly less than this value.
        cyan_stars : int, optional
            Filter Ayatan sculpture orders by exact Cyan Stars count.
        cyan_stars_lt : int, optional
            Filter Ayatan sculpture orders with Cyan Stars strictly less than this value.
        subtype : Subtype | str, optional
            Filter orders by item subtype (e.g., ``Subtype.radiant``).

        Returns
        -------
        TopOrders
            Object containing ``.buy`` (top 5 buy orders) and ``.sell`` (top 5 sell orders).

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     top = await tenno.items.get_top_orders("blind_rage", rank=10)
        ...     for order in top.sell:
        ...         print(order.user.ingame_name, order.platinum, "plat (rank", order.rank, ")")
        """
        return await self._get_top_orders(
            url_name,
            platform=platform,
            rank=rank,
            rank_lt=rank_lt,
            charges=charges,
            charges_lt=charges_lt,
            amber_stars=amber_stars,
            amber_stars_lt=amber_stars_lt,
            cyan_stars=cyan_stars,
            cyan_stars_lt=cyan_stars_lt,
            subtype=subtype,
        )
