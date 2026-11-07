"""Module containing constants used by PyTenno."""

from typing import Literal

API_ROOT: str = "https://api.warframe.market/v2"
"""Root URL for the Warframe.market v2 REST API."""

V1_API_ROOT: str = "https://api.warframe.market/v1"
"""Root URL for legacy Warframe.market v1 endpoints (e.g., auctions)."""

WS_ROOT: str = "wss://ws.warframe.market/socket"
"""Root URL for the Warframe.market v2 WebSocket server."""

ASSETS_ROOT: str = "https://warframe.market/static/assets/"
"""Root URL for static assets (icons, thumbnails, animations)."""

ValidLanguages = Literal[
    "ko",
    "ru",
    "de",
    "fr",
    "pt",
    "zh-hans",
    "zh-hant",
    "es",
    "it",
    "pl",
    "uk",
    "en",
]

ValidPlatforms = Literal["pc", "ps4", "xbox", "switch", "mobile"]
