"""Data models for Warframe.market v2 missions, NPCs, versions, and showcase."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ..utils import parse_iso_datetime
from .enums import ItemRarity, RelicQuality, Rotation, Stage, Subtype


@dataclass
class MissionI18N:
    """Localized metadata for a mission."""

    name: str
    icon: Optional[str] = None
    thumb: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "MissionI18N":
        return cls(
            name=data.get("name", ""),
            icon=data.get("icon"),
            thumb=data.get("thumb"),
        )


@dataclass
class Mission:
    """Represents a mission returned by ``GET /v2/missions``."""

    id: str
    """Unique identifier of the mission."""
    slug: str
    """URL-friendly slug of the mission."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    i18n: dict[str, MissionI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[MissionI18N]:
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
        """Localized mission name."""
        info = self._primary_i18n()
        return info.name if info else self.slug

    @property
    def icon(self) -> Optional[str]:
        """Localized icon asset path."""
        info = self._primary_i18n()
        return info.icon if info else None

    @property
    def thumb(self) -> Optional[str]:
        """Localized thumbnail asset path."""
        info = self._primary_i18n()
        return info.thumb if info else None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Mission":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: MissionI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and "name" in data:
            i18n["en"] = MissionI18N(
                name=data.get("name", ""),
                icon=data.get("icon"),
                thumb=data.get("thumb"),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            i18n=i18n,
        )


@dataclass
class NpcI18N:
    """Localized metadata for an NPC."""

    name: str
    icon: Optional[str] = None
    thumb: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "NpcI18N":
        return cls(
            name=data.get("name", ""),
            icon=data.get("icon"),
            thumb=data.get("thumb"),
        )


@dataclass
class Npc:
    """Represents an NPC returned by ``GET /v2/npcs``."""

    id: str
    """Unique identifier of the NPC."""
    slug: str
    """URL-friendly slug of the NPC."""
    game_ref: str = ""
    """Internal Warframe game reference path."""
    i18n: dict[str, NpcI18N] = field(default_factory=dict)
    """Localized metadata keyed by language code."""

    def _primary_i18n(self, lang: str = "en") -> Optional[NpcI18N]:
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
        """Localized NPC name."""
        info = self._primary_i18n()
        return info.name if info else self.slug

    @property
    def icon(self) -> Optional[str]:
        """Localized icon asset path."""
        info = self._primary_i18n()
        return info.icon if info else None

    @property
    def thumb(self) -> Optional[str]:
        """Localized thumbnail asset path."""
        info = self._primary_i18n()
        return info.thumb if info else None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Npc":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: NpcI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        if not i18n and "name" in data:
            i18n["en"] = NpcI18N(
                name=data.get("name", ""),
                icon=data.get("icon"),
                thumb=data.get("thumb"),
            )
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug") or data.get("url_name", ""),
            game_ref=data.get("gameRef") or data.get("game_ref", ""),
            i18n=i18n,
        )


@dataclass
class VersionsApps:
    """Mobile application version identifiers returned by ``GET /v2/versions``."""

    ios: str = ""
    android: str = ""
    min_ios: str = ""
    min_android: str = ""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "VersionsApps":
        return cls(
            ios=data.get("ios", ""),
            android=data.get("android", ""),
            min_ios=data.get("minIos") or data.get("min_ios", ""),
            min_android=data.get("minAndroid") or data.get("min_android", ""),
        )


@dataclass
class VersionsCollections:
    """Manifest collection version hashes returned by ``GET /v2/versions``."""

    items: str = ""
    rivens: str = ""
    liches: str = ""
    sisters: str = ""
    missions: str = ""
    npcs: str = ""
    locations: str = ""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "VersionsCollections":
        return cls(
            items=data.get("items", ""),
            rivens=data.get("rivens", ""),
            liches=data.get("liches", ""),
            sisters=data.get("sisters", ""),
            missions=data.get("missions", ""),
            npcs=data.get("npcs", ""),
            locations=data.get("locations", ""),
        )


@dataclass
class Versions:
    """Server resource and manifest versions returned by ``GET /v2/versions``."""

    id: str
    apps: VersionsApps
    collections: VersionsCollections
    updated_at: Optional[datetime] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Versions":
        return cls(
            id=data.get("id", ""),
            apps=VersionsApps._from_data(data.get("apps") or {}),
            collections=VersionsCollections._from_data(data.get("collections") or {}),
            updated_at=parse_iso_datetime(data.get("updatedAt") or data.get("updated_at")),
        )


@dataclass
class DashboardShowcaseI18N:
    """Localized title and description for the dashboard showcase."""

    title: str
    description: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "DashboardShowcaseI18N":
        return cls(
            title=data.get("title", ""),
            description=data.get("description"),
        )


@dataclass
class DashboardShowcaseItem:
    """Featured item card in the dashboard showcase."""

    item: str
    background: str
    big_card: bool = False

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "DashboardShowcaseItem":
        return cls(
            item=data.get("item", ""),
            background=data.get("background", ""),
            big_card=bool(data.get("bigCard", data.get("big_card", False))),
        )


@dataclass
class DashboardShowcase:
    """Featured items showcase returned by ``GET /v2/dashboard/showcase``."""

    i18n: dict[str, DashboardShowcaseI18N] = field(default_factory=dict)
    items: list[DashboardShowcaseItem] = field(default_factory=list)

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "DashboardShowcase":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: DashboardShowcaseI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        items = [DashboardShowcaseItem._from_data(i) for i in (data.get("items") or [])]
        return cls(i18n=i18n, items=items)


# Backward-compatible aliases
PartialMission = Mission
DroptableNPC = Npc


@dataclass
class DroptableRelic:
    """Represents a relic drop in a mission."""

    id: str
    rarity: ItemRarity
    rate: dict[RelicQuality, int | float]


@dataclass
class DroptableMission:
    """Represents a mission drop entry."""

    mission_id: str
    node_id: str
    rarity: ItemRarity
    rate: int | float
    item_subtype: Subtype
    rotation: Rotation
    stage: Stage
    relics: list[DroptableRelic]
    npc: list[DroptableNPC]
