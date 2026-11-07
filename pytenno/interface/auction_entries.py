"""Module holding the AuctionEntries interface class."""

from .._backends.auction_entries import AuctionEntriesBackend
from ..models.auctions import AuctionEntryExpanded
from ..models.bids import Bid


class AuctionEntries(AuctionEntriesBackend):
    """Interface for retrieving individual auction entries and bids by ID."""

    async def get_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Fetches a specific auction entry by its ID (`GET /v1/auctions/entry/{auction_id}`).

        Parameters
        ----------
        auction_id : str
            The unique ID of the auction entry.

        Returns
        -------
        AuctionEntryExpanded
        """
        return await self._get_by_id(auction_id)

    async def get_bids_by_id(self, auction_id: str) -> list[Bid]:
        """Fetches all bids for a specific auction entry by its ID (`GET /v1/auctions/entry/{auction_id}/bids`).

        Parameters
        ----------
        auction_id : str
            The unique ID of the auction entry.

        Returns
        -------
        list[Bid]
        """
        return await self._get_bids_by_id(auction_id)
