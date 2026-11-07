"""Data models for Warframe.market v2 Kuva Liches and Sisters of Parvos."""

from dataclasses import dataclass, field
from typing import Any, Optional

from ..utils import enum_or_raw
from .enums import Element


@dataclass
class LichWeaponI18N:
    """Localized metadata for a Kuva Lich or Sister of Parvos weapon."""

    name: str
    icon: str
    thumb: str
    wiki_link: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LichWeaponI18N":
        return cls(
            name=data.get("name") or data.get("item_name", ""),
            icon=data.get("icon", ""),
            thumb=data.get("thumb", ""),
            wiki_link=data.get("wikiLink") or data.get("wiki_link"),
        )


@dataclass
class LichWeapon:
    """Represents a Kuva Lich weapon returned by ``GET /v2/lich/weapons`` or ``GET /v2/lich/weapon/{slug}``."""

    id: str
    """Unique identifier of the weapon."""
    slug: str
    """URL-friendly slug of the weapon (e.g., ``"kuva_bramma"``)."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    req_mastery_rank: int = 0
    """Required Mastery Rank."""
    i18n: dict[str, LichWeaponI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[LichWeaponI18N]:
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
    def _from_data(cls, data: dict[str, Any]) -> "LichWeapon":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: LichWeaponI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and ("item_name" in data or "icon" in data):
            i18n["en"] = LichWeaponI18N(
                name=data.get("item_name", ""),
                icon=data.get("icon", ""),
                thumb=data.get("thumb", ""),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            req_mastery_rank=int(data.get("reqMasteryRank", data.get("mastery_level", 0))),
            i18n=i18n,
        )


@dataclass
class LichEphemeraI18N:
    """Localized metadata for a Kuva Lich or Sister of Parvos ephemera."""

    name: str
    icon: str
    thumb: str

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LichEphemeraI18N":
        return cls(
            name=data.get("name") or data.get("item_name", ""),
            icon=data.get("icon", ""),
            thumb=data.get("thumb", ""),
        )


@dataclass
class LichEphemera:
    """Represents a Kuva Lich ephemera returned by ``GET /v2/lich/ephemeras``."""

    id: str
    """Unique identifier of the ephemera."""
    slug: str
    """URL-friendly slug of the ephemera (e.g., ``"vengeful_charge"``)."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    animation: str = ""
    """Relative asset path for the ephemera animation preview."""
    element: Element | str = Element.impact
    """Elemental type associated with the ephemera."""
    i18n: dict[str, LichEphemeraI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[LichEphemeraI18N]:
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
        """Localized ephemera name."""
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

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LichEphemera":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: LichEphemeraI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and ("item_name" in data or "icon" in data):
            i18n["en"] = LichEphemeraI18N(
                name=data.get("item_name", ""),
                icon=data.get("icon", ""),
                thumb=data.get("thumb", ""),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            animation=data.get("animation", ""),
            element=enum_or_raw(Element, data.get("element", "impact")),
            i18n=i18n,
        )


@dataclass
class LichQuirkI18N:
    """Localized metadata for a Kuva Lich or Sister of Parvos quirk."""

    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    thumb: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LichQuirkI18N":
        return cls(
            name=data.get("name") or data.get("item_name", ""),
            description=data.get("description"),
            icon=data.get("icon"),
            thumb=data.get("thumb"),
        )


@dataclass
class LichQuirk:
    """Represents a Kuva Lich quirk returned by ``GET /v2/lich/quirks``."""

    id: str
    """Unique identifier of the quirk."""
    slug: str
    """URL-friendly slug of the quirk."""
    group: Optional[str] = None
    """Quirk group."""
    i18n: dict[str, LichQuirkI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[LichQuirkI18N]:
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
        """Localized quirk name."""
        info = self._primary_i18n()
        return info.name if info else self.slug

    @property
    def item_name(self) -> str:
        """Backward-compatible alias for :attr:`name`."""
        return self.name

    @property
    def description(self) -> Optional[str]:
        """Localized quirk description."""
        info = self._primary_i18n()
        return info.description if info else None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LichQuirk":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: LichQuirkI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and ("item_name" in data or "description" in data):
            i18n["en"] = LichQuirkI18N(
                name=data.get("item_name", ""),
                description=data.get("description"),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            group=data.get("group"),
            i18n=i18n,
        )


@dataclass
class SisterWeapon(LichWeapon):
    """Represents a Sister of Parvos weapon returned by ``GET /v2/sister/weapons``."""


@dataclass
class SisterEphemera(LichEphemera):
    """Represents a Sister of Parvos ephemera returned by ``GET /v2/sister/ephemeras``."""


@dataclass
class SisterQuirk(LichQuirk):
    """Represents a Sister of Parvos quirk returned by ``GET /v2/sister/quirks``."""
