"""Data models for Warframe.market v2 locations."""

from dataclasses import dataclass, field
from typing import Any, Optional

from ..utils import enum_or_raw
from .enums import Faction


@dataclass
class LocationI18N:
    """Localized metadata for a location."""

    node_name: str
    system_name: Optional[str] = None
    icon: str = ""
    thumb: str = ""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "LocationI18N":
        return cls(
            node_name=data.get("nodeName") or data.get("node_name", ""),
            system_name=data.get("systemName") or data.get("system_name") or data.get("name"),
            icon=data.get("icon", ""),
            thumb=data.get("thumb", ""),
        )


@dataclass
class Location:
    """Represents a location returned by ``GET /v2/locations``."""

    id: str
    """Unique identifier of the location."""
    slug: str
    """URL-friendly slug of the location."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    faction: Optional[Faction | str] = None
    """Faction controlling the location."""
    min_level: Optional[int] = None
    """Minimum enemy level on this node."""
    max_level: Optional[int] = None
    """Maximum enemy level on this node."""
    i18n: dict[str, LocationI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[LocationI18N]:
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
    def node_name(self) -> str:
        """Localized node name (e.g., ``"Hydron"``)."""
        info = self._primary_i18n()
        return info.node_name if info else self.slug

    @property
    def system_name(self) -> Optional[str]:
        """Localized planet/system name (e.g., ``"Sedna"``)."""
        info = self._primary_i18n()
        return info.system_name if info else None

    @property
    def name(self) -> str:
        """Backward-compatible alias returning :attr:`system_name` or :attr:`node_name`."""
        return self.system_name or self.node_name

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
    def _from_data(cls, data: dict[str, Any]) -> "Location":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: LocationI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and ("node_name" in data or "name" in data):
            i18n["en"] = LocationI18N(
                node_name=data.get("node_name", ""),
                system_name=data.get("name"),
                icon=data.get("icon", ""),
                thumb=data.get("thumb", ""),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            faction=enum_or_raw(Faction, data.get("faction")),
            min_level=data.get("minLevel", data.get("min_level")),
            max_level=data.get("maxLevel", data.get("max_level")),
            i18n=i18n,
        )
