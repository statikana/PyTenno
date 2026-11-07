"""Data models for Warframe.market v2 items and item sets."""

from dataclasses import dataclass, field
from typing import Any, Optional

from ..utils import enum_or_raw
from .enums import ItemRarity, Subtype


@dataclass
class ItemI18N:
    """Localized metadata for an item in a specific language (`i18n` map entry)."""

    name: str
    """Localized display name of the item."""
    icon: str
    """Relative asset path for the item's icon."""
    thumb: Optional[str] = None
    """Relative asset path for the item's thumbnail."""
    sub_icon: Optional[str] = None
    """Relative asset path for the item's sub-icon, if any."""
    description: Optional[str] = None
    """Localized description of the item."""
    wiki_link: Optional[str] = None
    """URL to the Warframe Wiki page for the item."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "ItemI18N":
        return cls(
            name=data.get("name", ""),
            icon=data.get("icon", ""),
            thumb=data.get("thumb"),
            sub_icon=data.get("subIcon") or data.get("sub_icon"),
            description=data.get("description"),
            wiki_link=data.get("wikiLink") or data.get("wiki_link"),
        )


@dataclass
class ItemShort:
    """Represents the compact v2 item model returned by ``GET /v2/items``."""

    id: str
    """Unique identifier of the item."""
    slug: str
    """URL-friendly slug of the item (e.g., ``"nikana_prime_set"``)."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    tags: list[str] = field(default_factory=list)
    """Categorization tags for the item."""
    i18n: dict[str, ItemI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code (e.g., ``"en"``)."""
    bulk_tradable: Optional[bool] = None
    """Whether the item can be traded in bulk."""
    subtypes: list[Subtype | str] = field(default_factory=list)
    """Available subtypes for the item (e.g., relic refinements)."""
    max_rank: Optional[int] = None
    """Maximum rank for mods/arcanes."""
    max_charges: Optional[int] = None
    """Maximum charges (e.g., Requiem mods / Parazon mods)."""
    max_amber_stars: Optional[int] = None
    """Maximum Amber Stars for Ayatan sculptures."""
    max_cyan_stars: Optional[int] = None
    """Maximum Cyan Stars for Ayatan sculptures."""
    base_endo: Optional[int] = None
    """Base Endo value for Ayatan sculptures."""
    endo_multiplier: Optional[float] = None
    """Endo socket multiplier for Ayatan sculptures."""
    ducats: Optional[int] = None
    """Ducat value for Prime parts."""
    vosfor: Optional[int] = None
    """Vosfor dissolution value for Arcanes."""
    req_mastery_rank: Optional[int] = None
    """Required Mastery Rank to trade/use the item."""
    vaulted: Optional[bool] = None
    """Whether the item is currently Prime Vaulted."""

    def _primary_i18n(self, lang: str = "en") -> Optional[ItemI18N]:
        if lang in self.i18n:
            return self.i18n[lang]
        if self.i18n:
            return next(iter(self.i18n.values()))
        return None

    @property
    def url_name(self) -> str:
        """Backward-compatible alias for :attr:`slug`."""
        return self.slug

    @property
    def name(self) -> str:
        """Localized display name (defaults to English or the client's requested language)."""
        info = self._primary_i18n()
        return info.name if info else self.slug

    @property
    def item_name(self) -> str:
        """Backward-compatible alias for :attr:`name`."""
        return self.name

    @property
    def icon(self) -> str:
        """Localized icon asset path."""
        info = self._primary_i18n()
        return info.icon if info else ""

    @property
    def thumb(self) -> Optional[str]:
        """Localized thumbnail asset path."""
        info = self._primary_i18n()
        return info.thumb if info else None

    @property
    def sub_icon(self) -> Optional[str]:
        """Localized sub-icon asset path."""
        info = self._primary_i18n()
        return info.sub_icon if info else None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "ItemShort":
        raw_i18n = data.get("i18n") or {}
        i18n = {k: ItemI18N._from_data(v) for k, v in raw_i18n.items() if isinstance(v, dict)}
        # Support legacy v1 payload fallback if needed
        if not i18n and ("item_name" in data or "thumb" in data):
            i18n["en"] = ItemI18N(
                name=data.get("item_name", ""),
                icon=data.get("icon", ""),
                thumb=data.get("thumb"),
                sub_icon=data.get("sub_icon"),
            )
        raw_subtypes = data.get("subtypes") or []
        subtypes = [enum_or_raw(Subtype, s) for s in raw_subtypes]
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            tags=list(data.get("tags") or []),
            i18n=i18n,
            bulk_tradable=data.get("bulkTradable", data.get("bulk_tradable")),
            subtypes=subtypes,
            max_rank=data.get("maxRank", data.get("mod_max_rank")),
            max_charges=data.get("maxCharges", data.get("max_charges")),
            max_amber_stars=data.get("maxAmberStars", data.get("max_amber_stars")),
            max_cyan_stars=data.get("maxCyanStars", data.get("max_cyan_stars")),
            base_endo=data.get("baseEndo", data.get("base_endo")),
            endo_multiplier=data.get("endoMultiplier", data.get("endo_multiplier")),
            ducats=data.get("ducats"),
            vosfor=data.get("vosfor"),
            req_mastery_rank=data.get("reqMasteryRank", data.get("mastery_level")),
            vaulted=data.get("vaulted"),
        )


@dataclass
class Item(ItemShort):
    """Represents the full v2 item model returned by ``GET /v2/item/{slug}``."""

    set_root: Optional[bool] = None
    """Whether this item is the root Set item (e.g., ``nikana_prime_set``)."""
    set_parts: list[str] = field(default_factory=list)
    """List of item IDs that belong to this item's set."""
    quantity_in_set: Optional[int] = None
    """How many copies of this part are required to complete the set."""
    rarity: Optional[ItemRarity | str] = None
    """Rarity of the item (for mods, relics, etc.)."""
    trading_tax: Optional[int] = None
    """In-game Credit tax required to trade this item."""
    tradable: Optional[bool] = None
    """Whether the item is tradable in-game."""

    @property
    def description(self) -> Optional[str]:
        """Localized item description."""
        info = self._primary_i18n()
        return info.description if info else None

    @property
    def wiki_link(self) -> Optional[str]:
        """Localized Warframe Wiki URL."""
        info = self._primary_i18n()
        return info.wiki_link if info else None

    @property
    def mastery_level(self) -> Optional[int]:
        """Backward-compatible alias for :attr:`req_mastery_rank`."""
        return self.req_mastery_rank

    @property
    def tax(self) -> Optional[int]:
        """Backward-compatible alias for :attr:`trading_tax`."""
        return self.trading_tax

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Item":
        base = ItemShort._from_data(data)
        rarity_raw = data.get("rarity")
        return cls(
            id=base.id,
            slug=base.slug,
            game_ref=base.game_ref,
            tags=base.tags,
            i18n=base.i18n,
            bulk_tradable=base.bulk_tradable,
            subtypes=base.subtypes,
            max_rank=base.max_rank,
            max_charges=base.max_charges,
            max_amber_stars=base.max_amber_stars,
            max_cyan_stars=base.max_cyan_stars,
            base_endo=base.base_endo,
            endo_multiplier=base.endo_multiplier,
            ducats=base.ducats,
            vosfor=base.vosfor,
            req_mastery_rank=base.req_mastery_rank,
            vaulted=base.vaulted,
            set_root=data.get("setRoot", data.get("set_root")),
            set_parts=list(data.get("setParts") or data.get("set_parts") or []),
            quantity_in_set=data.get("quantityInSet", data.get("quantity_for_set")),
            rarity=enum_or_raw(ItemRarity, rarity_raw),
            trading_tax=data.get("tradingTax", data.get("trading_tax")),
            tradable=data.get("tradable"),
        )


@dataclass
class ItemSet:
    """Represents an item set returned by ``GET /v2/item/{slug}/set``."""

    id: str
    """The ID of the queried item or set."""
    items: list[Item] = field(default_factory=list)
    """All items belonging to the set (including the set root and individual parts)."""

    @property
    def root(self) -> Optional[Item]:
        """Returns the root set item if present, otherwise the first item."""
        for item in self.items:
            if item.set_root:
                return item
        return self.items[0] if self.items else None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "ItemSet":
        items = [Item._from_data(it) for it in (data.get("items") or [])]
        return cls(id=data.get("id", ""), items=items)


# Backward-compatible aliases
PartialItem = ItemShort
FullItem = Item
