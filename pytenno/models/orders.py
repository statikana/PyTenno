"""Data models for Warframe.market v2 orders and transactions."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ..utils import enum_or_raw, parse_iso_datetime
from .enums import OrderType, Subtype
from .items import ItemShort
from .users import UserShort


@dataclass
class Order:
    """Represents a Warframe.market v2 order (without an embedded user)."""

    id: str
    """Unique identifier of the order."""
    type: OrderType
    """Whether this is a ``buy`` or ``sell`` order."""
    platinum: int
    """Unit price in Platinum."""
    quantity: int
    """Total quantity available or requested."""
    item_id: str = ""
    """The ID of the item associated with this order."""
    per_trade: Optional[int] = None
    """Minimum quantity per trade."""
    rank: Optional[int] = None
    """Rank of the mod or arcane."""
    charges: Optional[int] = None
    """Remaining charges (for Requiem mods)."""
    subtype: Optional[Subtype | str] = None
    """Subtype of the item (e.g., relic refinement or fish size)."""
    amber_stars: Optional[int] = None
    """Installed Amber Stars (for Ayatan sculptures)."""
    cyan_stars: Optional[int] = None
    """Installed Cyan Stars (for Ayatan sculptures)."""
    visible: bool = True
    """Whether the order is publicly visible."""
    created_at: Optional[datetime] = None
    """When the order was created."""
    updated_at: Optional[datetime] = None
    """When the order was last updated."""
    group: Optional[str] = None
    """Order group name, if any."""
    item: Optional[ItemShort] = None
    """Optional resolved item metadata if attached or returned by legacy endpoints."""

    @property
    def order_type(self) -> OrderType:
        """Backward-compatible alias for :attr:`type`."""
        return self.type

    @property
    def creation_date(self) -> Optional[datetime]:
        """Backward-compatible alias for :attr:`created_at`."""
        return self.created_at

    @property
    def last_update(self) -> Optional[datetime]:
        """Backward-compatible alias for :attr:`updated_at`."""
        return self.updated_at

    @property
    def mod_rank(self) -> Optional[int]:
        """Backward-compatible alias for :attr:`rank`."""
        return self.rank

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Order":
        raw_type = data.get("type") or data.get("order_type", "sell")
        raw_subtype = data.get("subtype") or data.get("subType")
        raw_item = data.get("item")
        return cls(
            id=data.get("id", ""),
            type=enum_or_raw(OrderType, raw_type),
            platinum=int(data.get("platinum", 0)),
            quantity=int(data.get("quantity", 0)),
            item_id=data.get("itemId") or data.get("item_id") or (raw_item.get("id", "") if isinstance(raw_item, dict) else ""),
            per_trade=data.get("perTrade", data.get("per_trade")),
            rank=data.get("rank", data.get("mod_rank")),
            charges=data.get("charges"),
            subtype=enum_or_raw(Subtype, raw_subtype),
            amber_stars=data.get("amberStars", data.get("amber_stars")),
            cyan_stars=data.get("cyanStars", data.get("cyan_stars")),
            visible=bool(data.get("visible", True)),
            created_at=parse_iso_datetime(data.get("createdAt") or data.get("creation_date")),
            updated_at=parse_iso_datetime(data.get("updatedAt") or data.get("last_update")),
            group=data.get("group"),
            item=ItemShort._from_data(raw_item) if isinstance(raw_item, dict) else None,
        )


@dataclass
class OrderWithUser(Order):
    """Represents a Warframe.market v2 order that includes the owner's :class:`UserShort` info."""

    user: Optional[UserShort] = None
    """The user who posted the order."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "OrderWithUser":
        base = Order._from_data(data)
        raw_user = data.get("user")
        return cls(
            id=base.id,
            type=base.type,
            platinum=base.platinum,
            quantity=base.quantity,
            item_id=base.item_id,
            per_trade=base.per_trade,
            rank=base.rank,
            charges=base.charges,
            subtype=base.subtype,
            amber_stars=base.amber_stars,
            cyan_stars=base.cyan_stars,
            visible=base.visible,
            created_at=base.created_at,
            updated_at=base.updated_at,
            group=base.group,
            item=base.item,
            user=UserShort._from_data(raw_user) if isinstance(raw_user, dict) else None,
        )


@dataclass
class TopOrders:
    """Represents the top 5 buy and top 5 sell orders returned by ``GET /v2/orders/item/{slug}/top``."""

    buy: list[OrderWithUser] = field(default_factory=list)
    """Top online buy orders (sorted by highest price)."""
    sell: list[OrderWithUser] = field(default_factory=list)
    """Top online sell orders (sorted by lowest price)."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "TopOrders":
        return cls(
            buy=[OrderWithUser._from_data(o) for o in (data.get("buy") or [])],
            sell=[OrderWithUser._from_data(o) for o in (data.get("sell") or [])],
        )


@dataclass
class TransactionItem:
    """Represents the item details inside a closed-order :class:`Transaction`."""

    id: Optional[str] = None
    rank: Optional[int] = None
    charges: Optional[int] = None
    subtype: Optional[Subtype | str] = None
    amber_stars: Optional[int] = None
    cyan_stars: Optional[int] = None

    @classmethod
    def _from_data(cls, data: Optional[dict[str, Any]]) -> Optional["TransactionItem"]:
        if not data or not isinstance(data, dict):
            return None
        return cls(
            id=data.get("id"),
            rank=data.get("rank"),
            charges=data.get("charges"),
            subtype=enum_or_raw(Subtype, data.get("subtype") or data.get("subType")),
            amber_stars=data.get("amberStars", data.get("amber_stars")),
            cyan_stars=data.get("cyanStars", data.get("cyan_stars")),
        )


@dataclass
class Transaction:
    """Represents a transaction record created when closing an order via ``POST /v2/order/{id}/close``."""

    id: str
    type: OrderType
    origin_id: str
    platinum: int
    quantity: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    item: Optional[TransactionItem] = None
    user: Optional[UserShort] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Transaction":
        raw_user = data.get("user")
        return cls(
            id=data.get("id", ""),
            type=enum_or_raw(OrderType, data.get("type", "sell")),
            origin_id=data.get("originId") or data.get("origin_id", ""),
            platinum=int(data.get("platinum", 0)),
            quantity=int(data.get("quantity", 0)),
            created_at=parse_iso_datetime(data.get("createdAt") or data.get("created_at")),
            updated_at=parse_iso_datetime(data.get("updatedAt") or data.get("updated_at")),
            item=TransactionItem._from_data(data.get("item")),
            user=UserShort._from_data(raw_user) if isinstance(raw_user, dict) else None,
        )


# Backward-compatible aliases
OrderRow = Order
ItemOrder = OrderWithUser
