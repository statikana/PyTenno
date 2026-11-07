"""Data models for Warframe.market auctions (Riven, Kuva Lich, Sister, and Kubrow)."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Union

from ..utils import enum_or_raw, parse_iso_datetime
from .enums import AuctionType, Element, Platform, Polarity, RivenStat
from .users import UserShort


@dataclass
class AuctionRivenStat:
    """Represents a single stat modifier on an auctioned Riven."""

    url_name: RivenStat | str
    """The stat identifier."""
    positive: bool
    """Whether the stat is positive."""
    value: int | float
    """The numerical value of the stat."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "AuctionRivenStat":
        return cls(
            url_name=enum_or_raw(RivenStat, data.get("url_name")),
            positive=bool(data.get("positive", True)),
            value=data.get("value", 0),
        )


@dataclass
class RivenAuction:
    """Represents a Riven item in an auction."""

    type: AuctionType
    """The type of the auction (`AuctionType.riven`)."""
    weapon_url_name: str
    """The URL slug of the weapon the Riven is for."""
    name: str
    """The suffix/prefix name of the Riven (e.g., ``"cori-gelicron"``)."""
    mastery_level: int
    """The Mastery Rank required to use the Riven."""
    re_rolls: int
    """The number of times the Riven has been re-rolled."""
    polarity: Polarity | str
    """The polarity of the Riven."""
    attributes: list[AuctionRivenStat]
    """The stats on the Riven."""
    mod_rank: int
    """The current upgrade rank of the Riven."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "RivenAuction":
        return cls(
            type=enum_or_raw(AuctionType, data.get("type", "riven")),
            weapon_url_name=data.get("weapon_url_name", ""),
            name=data.get("name", ""),
            mastery_level=int(data.get("mastery_level", 0)),
            re_rolls=int(data.get("re_rolls", 0)),
            polarity=enum_or_raw(Polarity, data.get("polarity", "any")),
            attributes=[
                AuctionRivenStat._from_data(attr) for attr in (data.get("attributes") or [])
            ],
            mod_rank=int(data.get("mod_rank", 0)),
        )


@dataclass
class LichAuction:
    """Represents a Kuva Lich or Sister of Parvos in an auction."""

    type: AuctionType
    """The type of the auction (`AuctionType.lich` or `AuctionType.sister`)."""
    weapon_url_name: str
    """The URL slug of the weapon."""
    element: Element | str
    """The elemental bonus type."""
    damage: int
    """The elemental bonus damage percentage."""
    having_ephemera: Optional[bool] = None
    """Whether the Lich/Sister has an ephemera."""
    quirk: Optional[str] = None
    """The quirk of the Lich/Sister, if any."""
    name: Optional[str] = None
    """The name of the Lich/Sister."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LichAuction":
        return cls(
            type=enum_or_raw(AuctionType, data.get("type", "lich")),
            weapon_url_name=data.get("weapon_url_name", ""),
            element=enum_or_raw(Element, data.get("element", "impact")),
            damage=int(data.get("damage", 0)),
            having_ephemera=data.get("having_ephemera"),
            quirk=data.get("quirk"),
            name=data.get("name"),
        )


@dataclass
class KubrowAuction:
    """Represents a Kubrow imprint in an auction."""

    type: AuctionType
    """The type of the auction (`AuctionType.kubrow`)."""
    name: str
    """The name/type of the Kubrow."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "KubrowAuction":
        return cls(
            type=enum_or_raw(AuctionType, data.get("type", "kubrow")),
            name=data.get("name", ""),
        )


def _item_from_data(
    item: dict[str, Any],
) -> Union[RivenAuction, LichAuction, KubrowAuction]:
    item_type = item.get("type")
    if item_type == "riven":
        return RivenAuction._from_data(item)
    if item_type in ("lich", "sister"):
        return LichAuction._from_data(item)
    return KubrowAuction._from_data(item)


@dataclass
class AuctionEntry:
    """Represents an auction entry on Warframe.market."""

    id: str
    minimal_reputation: int
    winner: Optional[str]
    private: bool
    visible: bool
    note_raw: str
    note: str
    owner: Union[UserShort, str]
    starting_price: int
    buyout_price: Optional[int]
    minimal_increment: Optional[int]
    is_direct_sell: bool
    top_bid: Optional[int]
    created: Optional[datetime]
    updated: Optional[datetime]
    platform: Platform | str
    closed: bool
    is_marked_for: Optional[str]
    marked_operation_at: Optional[datetime]
    item: Union[RivenAuction, LichAuction, KubrowAuction]
    crossplay: bool = True

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "AuctionEntry":
        raw_owner = data.get("owner")
        owner = (
            UserShort._from_data(raw_owner)
            if isinstance(raw_owner, dict)
            else (raw_owner or "")
        )
        return cls(
            id=data.get("id", ""),
            minimal_reputation=int(data.get("minimal_reputation", 0)),
            winner=data.get("winner"),
            private=bool(data.get("private", False)),
            visible=bool(data.get("visible", True)),
            note_raw=data.get("note_raw", ""),
            note=data.get("note", ""),
            owner=owner,
            starting_price=int(data.get("starting_price", 0)),
            buyout_price=data.get("buyout_price"),
            minimal_increment=data.get("minimal_increment"),
            is_direct_sell=bool(data.get("is_direct_sell", False)),
            top_bid=data.get("top_bid"),
            created=parse_iso_datetime(data.get("created")),
            updated=parse_iso_datetime(data.get("updated")),
            platform=enum_or_raw(Platform, data.get("platform", "pc")),
            closed=bool(data.get("closed", False)),
            is_marked_for=data.get("is_marked_for"),
            marked_operation_at=parse_iso_datetime(data.get("marked_operation_at")),
            item=_item_from_data(data.get("item") or {}),
            crossplay=bool(data.get("crossplay", True)),
        )


@dataclass
class AuctionEntryExpanded(AuctionEntry):
    """Represents an auction entry with an expanded :class:`UserShort` owner."""

    owner: UserShort
