"""Enumerations used across Warframe.market v2 models and interfaces."""

from enum import Enum


class Language(Enum):
    """Represents a supported language in the Warframe.market API."""

    ko = "ko"
    ru = "ru"
    de = "de"
    fr = "fr"
    pt = "pt"
    zh_hans = "zh-hans"
    zh_hant = "zh-hant"
    es = "es"
    it = "it"
    pl = "pl"
    uk = "uk"
    en = "en"


class Platform(Enum):
    """Represents a gaming platform supported by Warframe.market."""

    pc = "pc"
    ps4 = "ps4"
    xbox = "xbox"
    switch = "switch"
    mobile = "mobile"


class Subtype(Enum):
    """Represents an item subtype (relic refinement, blueprint/crafted, fish size, etc.)."""

    intact = "intact"
    exceptional = "exceptional"
    flawless = "flawless"
    radiant = "radiant"
    small = "small"
    medium = "medium"
    large = "large"
    blueprint = "blueprint"
    crafted = "crafted"


class Status(Enum):
    """Represents the online status of a user on Warframe.market."""

    ingame = "ingame"
    online = "online"
    offline = "offline"
    invisible = "invisible"


class ActivityType(Enum):
    """Represents the current in-game activity type of a user in v2."""

    UNKNOWN = "UNKNOWN"
    IDLE = "IDLE"
    ON_MISSION = "ON_MISSION"
    IN_DOJO = "IN_DOJO"
    IN_ORBITER = "IN_ORBITER"
    IN_RELAY = "IN_RELAY"


class OrderType(Enum):
    """Represents the type of an order (`buy` or `sell`)."""

    sell = "sell"
    buy = "buy"


class Role(Enum):
    """Represents a user's site role."""

    anonymous = "anonymous"
    user = "user"
    moderator = "moderator"
    admin = "admin"


class Tier(Enum):
    """Represents a user's Patreon/subscription tier on Warframe.market."""

    none = "none"
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    diamond = "diamond"


class Polarity(Enum):
    """Represents the polarity of a mod or Riven."""

    madurai = "madurai"
    vazarin = "vazarin"
    naramon = "naramon"
    zenurik = "zenurik"
    unairu = "unairu"
    penjaga = "penjaga"
    umbra = "umbra"
    any = "any"


class Element(Enum):
    """Represents an elemental bonus type on Kuva Lich or Sister of Parvos weapons/ephemeras."""

    impact = "impact"
    heat = "heat"
    cold = "cold"
    electricity = "electricity"
    toxin = "toxin"
    magnetic = "magnetic"
    radiation = "radiation"


class RivenWeaponGroup(Enum):
    """Represents a Riven weapon group."""

    primary = "primary"
    secondary = "secondary"
    melee = "melee"
    zaw = "zaw"
    sentinel = "sentinel"
    archgun = "archgun"
    kitgun = "kitgun"


class RivenWeaponType(Enum):
    """Represents a Riven weapon type."""

    rifle = "rifle"
    shotgun = "shotgun"
    pistol = "pistol"
    melee = "melee"
    zaw = "zaw"
    kitgun = "kitgun"
    archgun = "archgun"


class RivenUnit(Enum):
    """Represents a Riven attribute measurement unit."""

    percent = "percent"
    seconds = "seconds"
    multiply = "multiply"


class RivenAttributeGroup(Enum):
    """Represents a Riven attribute UI grouping."""

    default = "default"
    melee = "melee"
    top = "top"


class Faction(Enum):
    """Represents a faction in Warframe."""

    infested = "infested"
    grineer = "grineer"
    corpus = "corpus"
    corrupted = "corrupted"
    orokin = "orokin"
    sentient = "sentient"
    narmer = "narmer"
    murmur = "murmur"
    tenno = "tenno"
    crossfire = "crossfire"


class ItemRarity(Enum):
    """Represents the rarity of an item or drop."""

    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    legendary = "legendary"
    peculiar = "peculiar"
    archon = "archon"
    amalgam = "amalgam"
    galvanized = "galvanized"
    primed = "primed"


class RelicQuality(Enum):
    """Represents the refinement quality of a Void Relic."""

    intact = "intact"
    exceptional = "exceptional"
    flawless = "flawless"
    radiant = "radiant"


class Rotation(Enum):
    """Represents the reward rotation of a mission."""

    a = "a"
    b = "b"
    c = "c"


class Stage(Enum):
    """Represents the bounty stage of a mission."""

    first = "1"
    second = "2"
    third = "3"
    fourth = "4"
    final = "final"


class AuctionType(Enum):
    """Represents the item category of an auction."""

    riven = "riven"
    lich = "lich"
    sister = "sister"
    kubrow = "kubrow"


class RivenStat(Enum):
    """Represents a Riven stat identifier."""

    ammo_maximum = "ammo_maximum"
    damage_vs_corpus = "damage_vs_corpus"
    damage_vs_grineer = "damage_vs_grineer"
    damage_vs_infested = "damage_vs_infested"
    cold_damage = "cold_damage"
    channeling_damage = "channeling_damage"
    channeling_efficiency = "channeling_efficiency"
    combo_duration = "combo_duration"
    critical_chance = "critical_chance"
    critical_chance_on_slide_attack = "critical_chance_on_slide_attack"
    critical_damage = "critical_damage"
    base_damage_or_melee_damage = "base_damage_/_melee_damage"
    electric_damage = "electric_damage"
    heat_damage = "heat_damage"
    finisher_damage = "finisher_damage"
    fire_rate_or_attack_speed = "fire_rate_/_attack_speed"
    projectile_speed = "projectile_speed"
    initial_combo = "initial_combo"
    impact_damage = "impact_damage"
    magazine_capacity = "magazine_capacity"
    heavy_attack_efficiency = "heavy_attack_efficiency"
    multishot = "multishot"
    toxin_damage = "toxin_damage"
    punch_through = "punch_through"
    puncture_damage = "puncture_damage"
    reload_speed = "reload_speed"
    range = "range"
    slash_damage = "slash_damage"
    status_chance = "status_chance"
    status_duration = "status_duration"
    weapon_recoil = "weapon_recoil"
    zoom = "zoom"
    chance_to_gain_extra_combo_count = "chance_to_gain_extra_combo_count"
    chance_to_gain_combo_count = "chance_to_gain_combo_count"
    corrosive = "corrosive"
    viral = "viral"
    magnetic = "magnetic"
    radiation = "radiation"
    gas = "gas"
    blast = "blast"


class DropSourceType(Enum):
    """Represents the type of drop source for an item."""

    relic = "relic"
    mission = "mission"
    npc = "npc"
