"""Backend for Warframe.market v2 user profiles and orders."""

from typing import Any, Optional

from ..models.enums import OrderType, Subtype
from ..models.orders import Order, OrderWithUser, Transaction
from ..models.users import User, UserPrivate
from .core import RequestBackend


class ProfileBackend(RequestBackend):
    """Backend methods for `/v2/me`, `/v2/user/...`, `/v2/orders/...`, and `/v2/order/...`."""

    async def _get_me(self) -> UserPrivate:
        data = await self._get("/me")
        return UserPrivate._from_data(data)

    async def _get_user(self, slug: str) -> User:
        data = await self._get(f"/user/{slug}")
        return User._from_data(data)

    async def _get_user_by_id(self, user_id: str) -> User:
        data = await self._get(f"/userId/{user_id}")
        return User._from_data(data)

    async def _get_recent_orders(self) -> list[OrderWithUser]:
        data = await self._get("/orders/recent")
        return [OrderWithUser._from_data(o) for o in data]

    async def _get_orders(self, slug: str) -> list[Order]:
        data = await self._get(f"/orders/user/{slug}")
        return [Order._from_data(o) for o in data]

    async def _get_orders_by_user_id(self, user_id: str) -> list[Order]:
        data = await self._get(f"/orders/userId/{user_id}")
        return [Order._from_data(o) for o in data]

    async def _get_my_orders(self) -> list[Order]:
        data = await self._get("/orders/my")
        return [Order._from_data(o) for o in data]

    async def _get_order(self, order_id: str) -> OrderWithUser:
        data = await self._get(f"/order/{order_id}")
        return OrderWithUser._from_data(data)

    async def _create_order(
        self,
        item_id: str,
        order_type: OrderType | str,
        platinum: int,
        quantity: int,
        visible: bool = True,
        per_trade: Optional[int] = None,
        rank: Optional[int] = None,
        charges: Optional[int] = None,
        subtype: Optional[Subtype | str] = None,
        amber_stars: Optional[int] = None,
        cyan_stars: Optional[int] = None,
    ) -> Order:
        type_str = order_type.value if isinstance(order_type, OrderType) else str(order_type)
        payload: dict[str, Any] = {
            "itemId": item_id,
            "type": type_str,
            "platinum": int(platinum),
            "quantity": int(quantity),
            "visible": bool(visible),
        }
        if per_trade is not None:
            payload["perTrade"] = int(per_trade)
        if rank is not None:
            payload["rank"] = int(rank)
        if charges is not None:
            payload["charges"] = int(charges)
        if subtype is not None:
            payload["subtype"] = subtype.value if isinstance(subtype, Subtype) else str(subtype)
        if amber_stars is not None:
            payload["amberStars"] = int(amber_stars)
        if cyan_stars is not None:
            payload["cyanStars"] = int(cyan_stars)

        data = await self._post("/order", **payload)
        return Order._from_data(data)

    async def _update_order(
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
        payload: dict[str, Any] = {}
        if platinum is not None:
            payload["platinum"] = int(platinum)
        if quantity is not None:
            payload["quantity"] = int(quantity)
        if per_trade is not None:
            payload["perTrade"] = int(per_trade)
        if rank is not None:
            payload["rank"] = int(rank)
        if charges is not None:
            payload["charges"] = int(charges)
        if subtype is not None:
            payload["subtype"] = subtype.value if isinstance(subtype, Subtype) else str(subtype)
        if amber_stars is not None:
            payload["amberStars"] = int(amber_stars)
        if cyan_stars is not None:
            payload["cyanStars"] = int(cyan_stars)
        if visible is not None:
            payload["visible"] = bool(visible)

        data = await self._patch(f"/order/{order_id}", **payload)
        return Order._from_data(data)

    async def _delete_order(self, order_id: str) -> str:
        data = await self._delete(f"/order/{order_id}")
        if isinstance(data, str):
            return data
        if isinstance(data, dict) and "order_id" in data:
            return str(data["order_id"])
        return order_id

    async def _close_order(self, order_id: str, quantity: int = 1) -> Transaction:
        data = await self._post(f"/order/{order_id}/close", quantity=int(quantity))
        return Transaction._from_data(data)
