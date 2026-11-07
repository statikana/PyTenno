"""Module containing the PyTenno client class."""

from typing import Optional

from aiohttp import ClientSession

from .interface.auction_entries import AuctionEntries
from .interface.auctions import Auctions
from .interface.auth import Auth
from .interface.items import Items
from .interface.liches import Liches, Sisters
from .interface.misc import Misc
from .interface.profile import Orders, Profile, Users
from .interface.rivens import Rivens
from .models.enums import Language, Platform

DEFAULT_USER_AGENT = "pytenno/2.0.0 (+https://github.com/statikana/pytenno)"


class PyTenno:
    """Asynchronous client for the Warframe.market v2 API.

    Parameters
    ----------
    default_language : Language, optional
        Default language header (`Language`) sent with requests. Default is ``Language.en``.
    default_platform : Platform, optional
        Default platform header (`Platform`) sent with requests. Default is ``Platform.pc``.
    default_crossplay : bool, optional
        Default crossplay header (`Crossplay`) sent with requests. Default is ``True``.
    token : str, optional
        JWT / OAuth Bearer token for authenticated endpoints (`/v2/me`, `/v2/orders/my`, `/v2/order`).
    session : aiohttp.ClientSession, optional
        Optional pre-configured ``aiohttp.ClientSession`` to reuse.
    user_agent : str, optional
        Custom ``User-Agent`` header string. Defaults to ``"pytenno/2.0.0 (+https://github.com/statikana/pytenno)"``.

    Example
    -------
    >>> import asyncio
    >>> from pytenno import PyTenno
    >>>
    >>> async def main():
    ...     async with PyTenno() as tenno:
    ...         top = await tenno.items.get_top_orders("nikana_prime_set")
    ...         for order in top.sell:
    ...             print(order.user.ingame_name, order.platinum)
    >>>
    >>> asyncio.run(main())
    """

    def __init__(
        self,
        default_language: Language = Language.en,
        default_platform: Platform = Platform.pc,
        default_crossplay: bool = True,
        token: Optional[str] = None,
        session: Optional[ClientSession] = None,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.language = default_language
        self.platform = default_platform
        self.crossplay = default_crossplay
        self.token = token
        self.user_agent = user_agent

        headers: dict[str, str] = {
            "Language": (
                default_language.value
                if isinstance(default_language, Language)
                else str(default_language)
            ),
            "Platform": (
                default_platform.value
                if isinstance(default_platform, Platform)
                else str(default_platform)
            ),
            "Crossplay": "true" if default_crossplay else "false",
            "Accept": "application/json",
            "User-Agent": user_agent,
        }
        if token is not None:
            clean_token = (
                token[7:].strip()
                if token.lower().startswith("bearer ")
                else token[4:].strip()
                if token.lower().startswith("jwt ")
                else token.strip()
            )
            headers["Authorization"] = f"Bearer {clean_token}"
            self.token = clean_token

        self._owns_session = session is None
        self.session = session or ClientSession(headers=headers)
        if session is not None:
            self.session.headers.update(headers)

        self.auction_entries = AuctionEntries(self)
        """Interface for individual auction entry lookups (`tenno.auction_entries`)."""
        self.auctions = Auctions(self)
        """Interface for searching and creating auctions (`tenno.auctions`)."""
        self.auth = Auth(self)
        """Interface for account authentication (`tenno.auth`)."""
        self.items = Items(self)
        """Interface for items, item sets, and item orders (`tenno.items`)."""
        self.liches = Liches(self)
        """Interface for Kuva Lich weapons, ephemeras, and quirks (`tenno.liches`)."""
        self.sisters = Sisters(self)
        """Interface for Sister of Parvos weapons, ephemeras, and quirks (`tenno.sisters`)."""
        self.misc = Misc(self)
        """Interface for versions, locations, missions, NPCs, achievements, and showcase (`tenno.misc`)."""
        self.profile = Profile(self)
        """Interface for user profiles and order management (`tenno.profile`)."""
        self.orders: Orders = self.profile
        """Alias for :attr:`profile` providing direct access to order endpoints (`tenno.orders`)."""
        self.users: Users = self.profile
        """Alias for :attr:`profile` providing direct access to user endpoints (`tenno.users`)."""
        self.rivens = Rivens(self)
        """Interface for Riven weapons and attributes (`tenno.rivens`)."""

    def set_token(self, token: Optional[str]) -> None:
        """Updates or clears the ``Authorization: Bearer`` token on the active session.

        Parameters
        ----------
        token : Optional[str]
            The JWT / Bearer token string, or ``None`` to clear authentication.
        """
        self.token = token
        if token:
            clean_token = (
                token[7:].strip()
                if token.lower().startswith("bearer ")
                else token[4:].strip()
                if token.lower().startswith("jwt ")
                else token.strip()
            )
            self.token = clean_token
            self.session.headers["Authorization"] = f"Bearer {clean_token}"
        else:
            self.session.headers.pop("Authorization", None)

    async def __aenter__(self) -> "PyTenno":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        """Closes the underlying ``aiohttp.ClientSession``."""
        if not self.session.closed:
            await self.session.close()
