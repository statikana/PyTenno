"""Module holding the Profile and Orders interface classes."""

from typing import Optional

from .._backends.profile import ProfileBackend
from ..models.enums import OrderType, Subtype
from ..models.orders import Order, OrderWithUser, Transaction
from ..models.users import User, UserPrivate


class Profile(ProfileBackend):
    """Interface for Warframe.market v2 user profiles and order management."""

    async def get_me(self) -> UserPrivate:
        """Fetches the currently authenticated user's profile (`GET /v2/me`).

        Returns
        -------
        UserPrivate
            Full private profile details for the authenticated account.

        Example
        -------
        >>> async with PyTenno(token="...") as tenno:
        ...     me = await tenno.profile.get_me()
        ...     print(me.ingame_name, me.reputation, me.credits)
        """
        return await self._get_me()

    async def get_user(self, slug: str) -> User:
        """Fetches a public user profile by their slug (`GET /v2/user/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the user.

        Returns
        -------
        User
            The user's public profile.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     user = await tenno.profile.get_user("escanorsama1")
        ...     print(user.ingame_name, user.status.value, user.reputation)
        """
        return await self._get_user(slug)

    async def get_user_by_id(self, user_id: str) -> User:
        """Fetches a public user profile by their unique ID (`GET /v2/userId/{user_id}`).

        Parameters
        ----------
        user_id : str
            The user's unique Warframe.market ID.

        Returns
        -------
        User
            The user's public profile.
        """
        return await self._get_user_by_id(user_id)

    async def get_recent_orders(self) -> list[OrderWithUser]:
        """Fetches the most recent orders across Warframe.market (`GET /v2/orders/recent`).

        Returns up to 500 orders from the last 4 hours, sorted by ``created_at``.

        Returns
        -------
        list[OrderWithUser]
        """
        return await self._get_recent_orders()

    async def get_orders(self, slug: str) -> list[Order]:
        """Fetches all public orders for a user by their slug (`GET /v2/orders/user/{slug}`).

        Parameters
        ----------
        slug : str
            The URL-friendly slug of the user.

        Returns
        -------
        list[Order]
            All active orders belonging to the specified user.

        Example
        -------
        >>> async with PyTenno() as tenno:
        ...     orders = await tenno.profile.get_orders("escanorsama1")
        ...     for order in orders:
        ...         print(order.id, order.type.value, order.platinum)
        """
        return await self._get_orders(slug)

    async def get_orders_by_user_id(self, user_id: str) -> list[Order]:
        """Fetches all public orders for a user by their unique ID (`GET /v2/orders/userId/{user_id}`).

        Parameters
        ----------
        user_id : str
            The user's unique Warframe.market ID.

        Returns
        -------
        list[Order]
        """
        return await self._get_orders_by_user_id(user_id)

    async def get_my_orders(self) -> list[Order]:
        """Fetches all orders belonging to the currently authenticated user (`GET /v2/orders/my`).

        Returns
        -------
        list[Order]
        """
        return await self._get_my_orders()

    async def get_order(self, order_id: str) -> OrderWithUser:
        """Fetches a single order by its unique ID (`GET /v2/order/{order_id}`).

        Parameters
        ----------
        order_id : str
            The unique ID of the order.

        Returns
        -------
        OrderWithUser
        """
        return await self._get_order(order_id)

    async def create_order(
        self,
        item_id: str,
        order_type: OrderType,
        platinum: int,
        quantity: int,
        visible: bool = True,
        rank: Optional[int] = None,
        subtype: Optional[Subtype | str] = None,
        *,
        per_trade: Optional[int] = None,
        charges: Optional[int] = None,
        amber_stars: Optional[int] = None,
        cyan_stars: Optional[int] = None,
    ) -> Order:
        """Creates a new buy or sell order on the authenticated account (`POST /v2/order`).

        Parameters
        ----------
        item_id : str
            The ID of the item to list.
        order_type : OrderType
            ``OrderType.buy`` or ``OrderType.sell``.
        platinum : int
            Price per unit in Platinum.
        quantity : int
            Quantity of the item to buy or sell.
        visible : bool, optional
            Whether the order should be publicly visible. Default is ``True``.
        rank : int, optional
            Mod or Arcane rank, if applicable.
        subtype : Subtype | str, optional
            Item subtype (e.g., ``Subtype.radiant``), if applicable.
        per_trade : int, optional
            Minimum units per trade for bulk-tradable items.
        charges : int, optional
            Remaining charges (for Requiem mods).
        amber_stars : int, optional
            Installed Amber Stars (for Ayatan sculptures).
        cyan_stars : int, optional
            Installed Cyan Stars (for Ayatan sculptures).

        Returns
        -------
        Order
            The newly created order.

        Example
        -------
        >>> async with PyTenno(token="...") as tenno:
        ...     order = await tenno.profile.create_order(
        ...         item_id="56c3bbfc5d2f0202da32e943",
        ...         order_type=OrderType.sell,
        ...         platinum=60,
        ...         quantity=1,
        ...     )
        ...     print("Created order:", order.id)
        """
        return await self._create_order(
            item_id=item_id,
            order_type=order_type,
            platinum=platinum,
            quantity=quantity,
            visible=visible,
            per_trade=per_trade,
            rank=rank,
            charges=charges,
            subtype=subtype,
            amber_stars=amber_stars,
            cyan_stars=cyan_stars,
        )

    async def update_order(
        self,
        order_id: str,
        *,
        platinum: Optional[int] = None,
        quantity: Optional[int] = None,
        per_trade: Optional[int] = None,
        rank: Optional[int] = None,
        charges: Optional[int] = None,
        subtype: Optional[Subtype | str] = None,
        amber_stars: Optional[int] = None,
        cyan_stars: Optional[int] = None,
        visible: Optional[bool] = None,
    ) -> Order:
        """Updates an existing order (`PATCH /v2/order/{order_id}`).

        Parameters
        ----------
        order_id : str
            The ID of the order to update.
        platinum : int, optional
            Updated Platinum price.
        quantity : int, optional
            Updated quantity.
        per_trade : int, optional
            Updated minimum quantity per trade.
        rank : int, optional
            Updated mod/arcane rank.
        charges : int, optional
            Updated remaining charges.
        subtype : Subtype | str, optional
            Updated item subtype.
        amber_stars : int, optional
            Updated Amber Stars count.
        cyan_stars : int, optional
            Updated Cyan Stars count.
        visible : bool, optional
            Updated visibility status.

        Returns
        -------
        Order
            The updated order.
        """
        return await self._update_order(
            order_id,
            platinum=platinum,
            quantity=quantity,
            per_trade=per_trade,
            rank=rank,
            charges=charges,
            subtype=subtype,
            amber_stars=amber_stars,
            cyan_stars=cyan_stars,
            visible=visible,
        )

    async def delete_order(self, order_id: str) -> str:
        """Deletes an order by its ID (`DELETE /v2/order/{order_id}`).

        Parameters
        ----------
        order_id : str
            The ID of the order to delete.

        Returns
        -------
        str
            The deleted order's ID.
        """
        return await self._delete_order(order_id)

    async def close_order(self, order_id: str, quantity: int = 1) -> Transaction:
        """Closes part or all of an open order and records a transaction (`POST /v2/order/{order_id}/close`).

        Parameters
        ----------
        order_id : str
            The ID of the order to close.
        quantity : int, optional
            The number of units to subtract from the open order. Default is ``1``.

        Returns
        -------
        Transaction
            The recorded transaction.
        """
        return await self._close_order(order_id, quantity=quantity)


Orders = Profile
Users = Profile
