"""Data models for Warframe.market v2 Riven weapons and attributes."""

from dataclasses import dataclass, field
from typing import Any, Optional

from ..utils import enum_or_raw
from .enums import RivenAttributeGroup, RivenUnit, RivenWeaponGroup, RivenWeaponType


@dataclass
class RivenI18N:
    """Localized metadata for a Riven weapon."""

    name: str
    icon: str
    thumb: str
    wiki_link: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "RivenI18N":
        return cls(
            name=data.get("name", ""),
            icon=data.get("icon", ""),
            thumb=data.get("thumb", ""),
            wiki_link=data.get("wikiLink") or data.get("wiki_link"),
        )


@dataclass
class RivenItem:
    """Represents a Riven weapon returned by ``GET /v2/riven/weapons`` or ``GET /v2/riven/weapon/{slug}``."""

    id: str
    """Unique identifier of the Riven weapon."""
    slug: str
    """URL-friendly slug of the Riven weapon (e.g., ``"braton"``)."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    group: Optional[RivenWeaponGroup | str] = None
    """UI grouping of the weapon (e.g., ``primary``, ``secondary``, ``melee``)."""
    riven_type: Optional[RivenWeaponType | str] = None
    """Riven category type (e.g., ``rifle``, ``pistol``, ``shotgun``, ``melee``, ``zaw``, ``kitgun``, ``archgun``)."""
    disposition: float = 1.0
    """Riven disposition multiplier."""
    req_mastery_rank: int = 0
    """Required Mastery Rank."""
    i18n: dict[str, RivenI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[RivenI18N]:
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
        """Localized weapon name."""
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
    def thumb(self) -> str:
        """Localized thumbnail asset path."""
        info = self._primary_i18n()
        return info.thumb if info else ""

    @property
    def wiki_link(self) -> Optional[str]:
        """Localized Warframe Wiki link."""
        info = self._primary_i18n()
        return info.wiki_link if info else None

    @property
    def mastery_level(self) -> int:
        """Backward-compatible alias for :attr:`req_mastery_rank`."""
        return self.req_mastery_rank

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "RivenItem":
        raw_i18n = data.get("i18n") or {}
        i18n = {k: RivenI18N._from_data(v) for k, v in raw_i18n.items() if isinstance(v, dict)}
        if not i18n and ("item_name" in data or "icon" in data):
            i18n["en"] = RivenI18N(
                name=data.get("item_name", ""),
                icon=data.get("icon", ""),
                thumb=data.get("thumb", ""),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            group=enum_or_raw(RivenWeaponGroup, data.get("group")),
            riven_type=enum_or_raw(RivenWeaponType, data.get("rivenType") or data.get("riven_type")),
            disposition=float(data.get("disposition", 1.0)),
            req_mastery_rank=int(data.get("reqMasteryRank", data.get("mastery_level", 0))),
            i18n=i18n,
        )


@dataclass
class RivenAttributeI18N:
    """Localized metadata for a Riven attribute."""

    name: str
    icon: str
    thumb: str

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "RivenAttributeI18N":
        return cls(
            name=data.get("name") or data.get("effect", ""),
            icon=data.get("icon", ""),
            thumb=data.get("thumb", ""),
        )


@dataclass
class RivenAttribute:
    """Represents a Riven attribute returned by ``GET /v2/riven/attributes``."""

    id: str
    """Unique identifier of the Riven attribute."""
    slug: str
    """URL-friendly slug of the attribute (e.g., ``"critical_chance"``)."""
    game_ref: str = ""
    """Internal Warframe game reference name."""
    group: Optional[RivenAttributeGroup | str] = None
    """UI grouping of the attribute."""
    prefix: Optional[str] = None
    """Riven naming prefix when this stat is rolled."""
    suffix: Optional[str] = None
    """Riven naming suffix when this stat is rolled."""
    exclusive_to: list[RivenWeaponType | str] = field(default_factory=list)
    """Weapon types this attribute is restricted to."""
    positive_is_negative: bool = False
    """Whether a positive numerical value represents a penalty (e.g., recoil)."""
    positive_only: bool = False
    """Whether this attribute can only appear as a positive stat."""
    negative_only: bool = False
    """Whether this attribute can only appear as a negative stat."""
    unit: Optional[RivenUnit | str] = None
    """Measurement unit of the attribute."""
    i18n: dict[str, RivenAttributeI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[RivenAttributeI18N]:
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
        """Localized attribute name."""
        info = self._primary_i18n()
        return info.name if info else self.slug

    @property
    def effect(self) -> str:
        """Backward-compatible alias for :attr:`name`."""
        return self.name

    @property
    def icon(self) -> str:
        """Localized icon asset path."""
        info = self._primary_i18n()
        return info.icon if info else ""

    @property
    def thumb(self) -> str:
        """Localized thumbnail asset path."""
        info = self._primary_i18n()
        return info.thumb if info else ""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "RivenAttribute":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: RivenAttributeI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and "effect" in data:
            i18n["en"] = RivenAttributeI18N(
                name=data.get("effect", ""),
                icon=data.get("icon", ""),
                thumb=data.get("thumb", ""),
            )
        raw_excl = data.get("exclusiveTo") or data.get("exclusive_to") or []
        exclusive_to = [enum_or_raw(RivenWeaponType, x) for x in raw_excl]
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            group=enum_or_raw(RivenAttributeGroup, data.get("group")),
            prefix=data.get("prefix"),
            suffix=data.get("suffix"),
            exclusive_to=exclusive_to,
            positive_is_negative=bool(
                data.get("positiveIsNegative", data.get("positive_is_negative", False))
            ),
            positive_only=bool(data.get("positiveOnly", data.get("positive_only", False))),
            negative_only=bool(data.get("negativeOnly", data.get("negative_only", False))),
            unit=enum_or_raw(RivenUnit, data.get("unit") or data.get("units")),
            i18n=i18n,
        )


RivenWeapon = RivenItem
