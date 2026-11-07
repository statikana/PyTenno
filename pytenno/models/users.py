"""Data models for Warframe.market v2 users and profiles."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ..utils import enum_or_raw, parse_iso_datetime
from .enums import ActivityType, Language, Platform, Role, Status, Tier


@dataclass
class Activity:
    """Represents a user's current in-game activity in Warframe.market v2."""

    type: ActivityType | str = ActivityType.UNKNOWN
    """The type of activity (e.g., ``ON_MISSION``, ``IN_DOJO``)."""
    details: Optional[str] = None
    """Optional details about the activity."""
    started_at: Optional[datetime] = None
    """Timestamp when the activity started."""

    @classmethod
    def _from_data(cls, data: Optional[dict[str, Any]]) -> Optional["Activity"]:
        if not data or not isinstance(data, dict):
            return None
        return cls(
            type=enum_or_raw(ActivityType, data.get("type", "UNKNOWN")),
            details=data.get("details"),
            started_at=parse_iso_datetime(data.get("startedAt") or data.get("started_at")),
        )


@dataclass
class AchievementI18N:
    """Localized metadata for an achievement."""

    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    thumb: Optional[str] = None

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "AchievementI18N":
        return cls(
            name=data.get("name", ""),
            description=data.get("description"),
            icon=data.get("icon"),
            thumb=data.get("thumb"),
        )


@dataclass
class AchievementState:
    """User-specific progress state on an achievement."""

    featured: Optional[bool] = None
    hidden: Optional[bool] = None
    progress: Optional[int] = None
    completed_at: Optional[datetime] = None

    @classmethod
    def _from_data(cls, data: Optional[dict[str, Any]]) -> Optional["AchievementState"]:
        if not data or not isinstance(data, dict):
            return None
        return cls(
            featured=data.get("featured"),
            hidden=data.get("hidden"),
            progress=data.get("progress"),
            completed_at=parse_iso_datetime(data.get("completedAt") or data.get("completed_at")),
        )


@dataclass
class Achievement:
    """Represents a Warframe.market user achievement."""

    id: str
    slug: str
    type: str = ""
    secret: Optional[bool] = None
    reputation_bonus: Optional[int] = None
    goal: Optional[int] = None
    i18n: dict[str, AchievementI18N] = field(default_factory=dict)
    state: Optional[AchievementState] = None

    @property
    def name(self) -> str:
        """Localized achievement name."""
        if "en" in self.i18n:
            return self.i18n["en"].name
        if self.i18n:
            return next(iter(self.i18n.values())).name
        return self.slug

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "Achievement":
        raw_i18n = data.get("i18n") or {}
        i18n = {
            k: AchievementI18N._from_data(v)
            for k, v in raw_i18n.items()
            if isinstance(v, dict)
        }
        return cls(
            id=data.get("id", ""),
            slug=data.get("slug", ""),
            type=data.get("type", ""),
            secret=data.get("secret"),
            reputation_bonus=data.get("reputationBonus", data.get("reputation_bonus")),
            goal=data.get("goal"),
            i18n=i18n,
            state=AchievementState._from_data(data.get("state")),
        )


@dataclass
class LinkedAccounts:
    """Represents linked third-party accounts on a user's profile."""

    steam_profile: bool = False
    patreon_profile: bool = False
    xbox_profile: bool = False
    discord_profile: bool = False
    github_profile: bool = False

    @classmethod
    def _from_data(cls, data: Optional[dict[str, Any]]) -> "LinkedAccounts":
        if not data or not isinstance(data, dict):
            return cls()
        return cls(
            steam_profile=bool(data.get("steam_profile", data.get("steam", False))),
            patreon_profile=bool(data.get("patreon_profile", data.get("patreon", False))),
            xbox_profile=bool(data.get("xbox_profile", data.get("xbox", False))),
            discord_profile=bool(data.get("discord_profile", data.get("discord", False))),
            github_profile=bool(data.get("github_profile", data.get("github", False))),
        )


@dataclass
class UserShort:
    """Compact user representation embedded in orders and auctions."""

    id: str
    """Unique user ID."""
    ingame_name: str
    """User's in-game Warframe alias."""
    slug: str = ""
    """User's URL-friendly profile slug."""
    reputation: int = 0
    """User's reputation score on Warframe.market."""
    platform: Platform | str = Platform.pc
    """User's primary platform."""
    crossplay: bool = True
    """Whether the user has cross-platform trade enabled."""
    locale: Language | str = Language.en
    """User's preferred language locale."""
    status: Status | str = Status.offline
    """User's current online status."""
    avatar: Optional[str] = None
    """Relative asset URL to the user's avatar."""
    last_seen: Optional[datetime] = None
    """When the user was last active."""
    activity: Optional[Activity] = None
    """User's current in-game activity."""
    region: Optional[str] = None
    """Legacy region field."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "UserShort":
        return cls(
            id=data.get("id", ""),
            ingame_name=data.get("ingameName") or data.get("ingame_name", ""),
            slug=data.get("slug", ""),
            reputation=int(data.get("reputation", 0)),
            platform=enum_or_raw(Platform, data.get("platform", "pc")),
            crossplay=bool(data.get("crossplay", True)),
            locale=enum_or_raw(Language, data.get("locale", "en")),
            status=enum_or_raw(Status, data.get("status", "offline")),
            avatar=data.get("avatar"),
            last_seen=parse_iso_datetime(data.get("lastSeen") or data.get("last_seen")),
            activity=Activity._from_data(data.get("activity")),
            region=data.get("region"),
        )


@dataclass
class User(UserShort):
    """Public user profile returned by ``GET /v2/user/{slug}`` or ``GET /v2/userId/{id}``."""

    role: Role | str = Role.user
    """User's site role."""
    tier: Tier | str = Tier.none
    """User's subscription tier."""
    mastery_rank: Optional[int] = None
    """User's Warframe Mastery Rank."""
    about: Optional[str] = None
    """User's profile 'About' text (HTML/rendered)."""
    background: Optional[str] = None
    """Relative asset URL to the user's profile background."""
    achievement_showcase: list[Achievement] = field(default_factory=list)
    """Featured achievements on the user's profile."""
    banned: Optional[bool] = None
    """Whether the user is currently banned."""
    ban_until: Optional[datetime] = None
    """When the user's ban expires, if banned."""
    ban_message: Optional[str] = None
    """Reason for the ban, if banned."""
    warned: Optional[bool] = None
    """Whether the user has an active warning."""
    warned_message: Optional[str] = None
    """Warning message, if any."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "User":
        base = UserShort._from_data(data)
        showcase = [
            Achievement._from_data(a)
            for a in (data.get("achievementShowcase") or data.get("achievement_showcase") or [])
        ]
        return cls(
            id=base.id,
            ingame_name=base.ingame_name,
            slug=base.slug,
            reputation=base.reputation,
            platform=base.platform,
            crossplay=base.crossplay,
            locale=base.locale,
            status=base.status,
            avatar=base.avatar,
            last_seen=base.last_seen,
            activity=base.activity,
            region=base.region,
            role=enum_or_raw(Role, data.get("role", "user")),
            tier=enum_or_raw(Tier, data.get("tier", "none")),
            mastery_rank=data.get("masteryRank", data.get("masteryLevel", data.get("mastery_level"))),
            about=data.get("about"),
            background=data.get("background"),
            achievement_showcase=showcase,
            banned=data.get("banned"),
            ban_until=parse_iso_datetime(data.get("banUntil") or data.get("ban_until")),
            ban_message=data.get("banMessage") or data.get("ban_message") or data.get("ban_reason"),
            warned=data.get("warned"),
            warned_message=data.get("warnedMessage") or data.get("warned_message"),
        )


@dataclass
class UserPrivate(User):
    """Authenticated user profile returned by ``GET /v2/me`` or sign-in."""

    about_raw: Optional[str] = None
    """Raw markdown of the user's 'About' section."""
    check_code: Optional[str] = None
    """Account verification code for forum/in-game verification."""
    created_at: Optional[datetime] = None
    """When the account was created."""
    credits: Optional[int] = None
    """Account credits balance."""
    has_email: Optional[bool] = None
    """Whether an email address is linked."""
    linked_accounts: LinkedAccounts = field(default_factory=LinkedAccounts)
    """Linked external accounts."""
    ignore_list: list[str] = field(default_factory=list)
    """List of ignored user IDs."""
    reviews_left: Optional[int] = None
    """Remaining daily reputation reviews."""
    subscription: Optional[bool] = None
    """Whether the user has an active subscription."""
    sync_locale: Optional[bool] = None
    """Whether locale is synced across devices."""
    sync_theme: Optional[bool] = None
    """Whether UI theme is synced across devices."""
    theme: Optional[str] = None
    """Preferred UI theme."""
    unread_messages: Optional[int] = None
    """Count of unread private messages."""
    unread_notifications: Optional[int] = None
    """Count of unread notifications."""
    verification: Optional[bool] = None
    """Whether the user is verified."""
    written_reviews: Optional[int] = None
    """Number of written reviews."""
    anonymous: Optional[bool] = None
    """Whether the session is anonymous."""
    delete_at: Optional[datetime] = None
    """Scheduled deletion timestamp, if account deletion is in progress."""
    delete_in_progress: Optional[bool] = None
    """Whether account deletion is in progress."""

    @classmethod
    def _from_data(cls, data: dict[str, Any]) -> "UserPrivate":
        pub = User._from_data(data)
        return cls(
            id=pub.id,
            ingame_name=pub.ingame_name,
            slug=pub.slug,
            reputation=pub.reputation,
            platform=pub.platform,
            crossplay=pub.crossplay,
            locale=pub.locale,
            status=pub.status,
            avatar=pub.avatar,
            last_seen=pub.last_seen,
            activity=pub.activity,
            region=pub.region,
            role=pub.role,
            tier=pub.tier,
            mastery_rank=pub.mastery_rank,
            about=pub.about,
            background=pub.background,
            achievement_showcase=pub.achievement_showcase,
            banned=pub.banned,
            ban_until=pub.ban_until,
            ban_message=pub.ban_message,
            warned=pub.warned,
            warned_message=pub.warned_message,
            about_raw=data.get("aboutRaw") or data.get("about_raw"),
            check_code=data.get("checkCode") or data.get("check_code"),
            created_at=parse_iso_datetime(data.get("createdAt") or data.get("created_at")),
            credits=data.get("credits"),
            has_email=data.get("hasEmail", data.get("has_mail")),
            linked_accounts=LinkedAccounts._from_data(
                data.get("linkedAccounts") or data.get("linked_accounts")
            ),
            ignore_list=list(data.get("ignoreList") or data.get("ignore_list") or []),
            reviews_left=data.get("reviewsLeft", data.get("reviews_left")),
            subscription=data.get("subscription"),
            sync_locale=data.get("syncLocale", data.get("sync_locale")),
            sync_theme=data.get("syncTheme", data.get("sync_theme")),
            theme=data.get("theme"),
            unread_messages=data.get("unreadMessages", data.get("unread_messages")),
            unread_notifications=data.get(
                "unreadNotifications", data.get("unread_notifications")
            ),
            verification=data.get("verification"),
            written_reviews=data.get("writtenReviews", data.get("written_reviews")),
            anonymous=data.get("anonymous"),
            delete_at=parse_iso_datetime(data.get("deleteAt") or data.get("delete_at")),
            delete_in_progress=data.get("deleteInProgress", data.get("delete_in_progress")),
        )


# Backward-compatible aliases
CurrentUser = UserPrivate
PartialUser = User
