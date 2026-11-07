"""Backend for Warframe.market auction search and creation."""

from typing import Literal, Optional, Union

from ..models.auctions import (
    AuctionEntryExpanded,
    KubrowAuction,
    LichAuction,
    RivenAuction,
)
from ..models.enums import Element, Platform, Polarity, RivenStat
from .core import RequestBackend


class AuctionsBackend(RequestBackend):
    """Backend methods for `/v1/auctions/...` endpoints."""

    async def _create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: int = 0,
        minimal_increment: int = 1,
        private: bool = False,
    ) -> AuctionEntryExpanded:
        data = await self._post(
            "/auctions/create",
            api_version="v1",
            item=item.__dict__,
            note=note,
            starting_price=starting_price,
            buyout_price=buyout_price,
            minimal_reputation=minimal_reputation,
            minimal_increment=minimal_increment,
            private=private,
        )
        return AuctionEntryExpanded._from_data(data["auction"])

    async def _find_riven_auctions(
        self,
        platform: Optional[Platform] = None,
        weapon_url_name: Optional[str] = None,
        mastery_rank_min: Optional[int] = None,
        mastery_rank_max: Optional[int] = None,
        re_rolls_min: Optional[int] = None,
        re_rolls_max: Optional[int] = None,
        positive_stats: Optional[list[RivenStat]] = None,
        negative_stats: Optional[list[RivenStat]] = None,
        polarity: Optional[Polarity] = None,
        mod_rank: Optional[Literal["any", "maxed"]] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = None,
        operation: Optional[Literal["anyOf", "allOf"]] = None,
        buyout_policy: Optional[Literal["with", "direct"]] = None,
    ) -> list[AuctionEntryExpanded]:
        headers = None
        if platform is not None:
            plat_str = platform.value if isinstance(platform, Platform) else str(platform)
            headers = {"Platform": plat_str}
        params = {
            "type": "riven",
            "weapon_url_name": weapon_url_name,
            "mastery_rank_min": mastery_rank_min,
            "mastery_rank_max": mastery_rank_max,
            "re_rolls_min": re_rolls_min,
            "re_rolls_max": re_rolls_max,
            "positive_stats": ",".join(
                s.value if isinstance(s, RivenStat) else str(s) for s in positive_stats
            )
            if positive_stats
            else None,
            "negative_stats": ",".join(
                s.value if isinstance(s, RivenStat) else str(s) for s in negative_stats
            )
            if negative_stats
            else None,
            "polarity": polarity.value if isinstance(polarity, Polarity) else polarity,
            "mod_rank": mod_rank,
            "sort_by": sort_by,
            "operation": operation,
            "buyout_policy": buyout_policy,
        }
        data = await self._get(
            "/auctions/search",
            params=params,
            headers=headers,
            api_version="v1",
        )
        return [
            AuctionEntryExpanded._from_data(auction)
            for auction in data["auctions"]
        ]

    async def _find_lich_auctions(
        self,
        platform: Optional[Platform | str] = None,
        weapon_url_name: Optional[str] = None,
        element: Optional[Element] = None,
        ephemera: Optional[bool] = None,
        damage_min: Optional[int] = None,
        damage_max: Optional[int] = None,
        quirk_url_name: Optional[str] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = "price_desc",
        buyout_policy: Optional[Literal["with", "direct"]] = None,
        auction_type: Literal["lich", "sister"] = "lich",
    ) -> list[AuctionEntryExpanded]:
        headers = None
        if platform is not None and str(platform) != "None":
            plat_str = platform.value if isinstance(platform, Platform) else str(platform)
            headers = {"Platform": plat_str}
        params = {
            "type": auction_type,
            "weapon_url_name": weapon_url_name,
            "element": element.value if isinstance(element, Element) else element,
            "having_ephemera": ephemera,
            "damage_min": damage_min,
            "damage_max": damage_max,
            "quirk": quirk_url_name,
            "sort_by": sort_by,
            "buyout_policy": buyout_policy,
        }
        data = await self._get(
            "/auctions/search",
            params=params,
            headers=headers,
            api_version="v1",
        )
        return [
            AuctionEntryExpanded._from_data(auction)
            for auction in data["auctions"]
        ]
