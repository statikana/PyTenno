"""Module holding the Auctions interface class."""

from typing import Literal, Optional, Union

from .._backends.auctions import AuctionsBackend
from ..models.auctions import (
    AuctionEntryExpanded,
    KubrowAuction,
    LichAuction,
    RivenAuction,
)
from ..models.enums import Element, Platform, Polarity, RivenStat


class Auctions(AuctionsBackend):
    """Interface for creating and searching Riven, Kuva Lich, and Sister of Parvos auctions."""

    async def create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: int = 0,
        minimal_increment: int = 1,
        private: bool = False,
    ) -> AuctionEntryExpanded:
        """Creates a new auction on Warframe.market.

        Parameters
        ----------
        item : RivenAuction | LichAuction | KubrowAuction
            The item to auction.
        note : str
            Description note for the auction.
        starting_price : int
            Starting bid price in Platinum.
        buyout_price : int
            Instant buyout price in Platinum.
        minimal_reputation : int, optional
            Minimum reputation required to bid. Default is ``0``.
        minimal_increment : int, optional
            Minimum bid increment in Platinum. Default is ``1``.
        private : bool, optional
            Whether the auction is private. Default is ``False``.

        Returns
        -------
        AuctionEntryExpanded
        """
        if starting_price > buyout_price:
            raise ValueError("Starting price cannot be higher than buyout price.")
        if minimal_increment < 1:
            raise ValueError("Minimal increment cannot be less than 1.")

        return await self._create_auction(
            item,
            note,
            starting_price,
            buyout_price,
            minimal_reputation,
            minimal_increment,
            private,
        )

    async def find_riven_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Optional[Platform] = None,
        mastery_rank_min: Optional[int] = None,
        mastery_rank_max: Optional[int] = None,
        re_rolls_min: Optional[int] = None,
        re_rolls_max: Optional[int] = None,
        positive_stats: Optional[list[RivenStat]] = None,
        negative_stats: Optional[list[RivenStat]] = None,
        polarity: Polarity = Polarity.any,
        mod_rank: Optional[Literal["any", "maxed"]] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = None,
        operation: Optional[Literal["anyOf", "allOf"]] = None,
        buyout_policy: Optional[Literal["with", "direct"]] = None,
    ) -> list[AuctionEntryExpanded]:
        """Searches Riven auctions matching the specified criteria.

        Parameters
        ----------
        weapon_url_name : str
            The URL-friendly slug of the weapon (e.g., ``"braton"``).
        platform : Platform, optional
            Override the client's default platform.
        mastery_rank_min : int, optional
            Minimum Mastery Rank of the Riven.
        mastery_rank_max : int, optional
            Maximum Mastery Rank of the Riven.
        re_rolls_min : int, optional
            Minimum number of re-rolls.
        re_rolls_max : int, optional
            Maximum number of re-rolls.
        positive_stats : list[RivenStat], optional
            Required positive stats (up to 3).
        negative_stats : list[RivenStat], optional
            Required negative stat (up to 1).
        polarity : Polarity, optional
            Polarity filter. Default is ``Polarity.any``.
        mod_rank : Literal["any", "maxed"], optional
            Filter by upgrade rank.
        sort_by : Literal["price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"], optional
            Sort order for results.
        operation : Literal["anyOf", "allOf"], optional
            Matching operation for stats.
        buyout_policy : Literal["with", "direct"], optional
            Filter by buyout policy.

        Returns
        -------
        list[AuctionEntryExpanded]
        """
        if positive_stats is not None and len(positive_stats) > 3:
            raise ValueError("The amount of positive stats cannot be greater than 3.")
        if negative_stats is not None and len(negative_stats) > 3:
            raise ValueError("The amount of negative stats cannot be greater than 3.")
        if (
            mastery_rank_min is not None
            and mastery_rank_max is not None
            and mastery_rank_min > mastery_rank_max
        ):
            raise ValueError(
                "The mastery rank min cannot be greater than the mastery rank max."
            )
        if (
            re_rolls_min is not None
            and re_rolls_max is not None
            and re_rolls_min > re_rolls_max
        ):
            raise ValueError(
                "The re-rolls min cannot be greater than the re-rolls max."
            )
        if mastery_rank_min is not None and mastery_rank_min < 0:
            raise ValueError("The mastery rank min cannot be less than 0.")
        if re_rolls_min is not None and re_rolls_min < 0:
            raise ValueError("The re-rolls min cannot be less than 0.")

        return await self._find_riven_auctions(
            platform=platform,
            weapon_url_name=weapon_url_name,
            mastery_rank_min=mastery_rank_min,
            mastery_rank_max=mastery_rank_max,
            re_rolls_min=re_rolls_min,
            re_rolls_max=re_rolls_max,
            positive_stats=positive_stats,
            negative_stats=negative_stats,
            polarity=polarity,
            mod_rank=mod_rank,
            sort_by=sort_by,
            operation=operation,
            buyout_policy=buyout_policy,
        )

    async def find_lich_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Optional[Platform] = None,
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
    ) -> list[AuctionEntryExpanded]:
        """Searches Kuva Lich auctions matching the specified criteria."""
        if (
            damage_min is not None
            and damage_max is not None
            and damage_min > damage_max
        ):
            raise ValueError("The damage min cannot be greater than the damage max.")
        if damage_min is not None and damage_min < 0:
            raise ValueError("The damage min cannot be less than 0.")
        if damage_max is not None and damage_max < 0:
            raise ValueError("The damage max cannot be less than 0.")

        return await self._find_lich_auctions(
            platform=platform,
            weapon_url_name=weapon_url_name,
            element=element,
            ephemera=ephemera,
            damage_min=damage_min,
            damage_max=damage_max,
            quirk_url_name=quirk_url_name,
            sort_by=sort_by,
            buyout_policy=buyout_policy,
            auction_type="lich",
        )

    async def find_sister_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Optional[Platform] = None,
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
    ) -> list[AuctionEntryExpanded]:
        """Searches Sister of Parvos auctions matching the specified criteria."""
        if (
            damage_min is not None
            and damage_max is not None
            and damage_min > damage_max
        ):
            raise ValueError("The damage min cannot be greater than the damage max.")
        if damage_min is not None and damage_min < 0:
            raise ValueError("The damage min cannot be less than 0.")
        if damage_max is not None and damage_max < 0:
            raise ValueError("The damage max cannot be less than 0.")

        return await self._find_lich_auctions(
            platform=platform,
            weapon_url_name=weapon_url_name,
            element=element,
            ephemera=ephemera,
            damage_min=damage_min,
            damage_max=damage_max,
            quirk_url_name=quirk_url_name,
            sort_by=sort_by,
            buyout_policy=buyout_policy,
            auction_type="sister",
        )
