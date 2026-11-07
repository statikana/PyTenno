"""Backend for Warframe.market auction entries."""

from ..models.auctions import AuctionEntryExpanded
from ..models.bids import Bid
from ..utils import parse_iso_datetime
from .core import RequestBackend


class AuctionEntriesBackend(RequestBackend):
    """Backend methods for `/v1/auctions/entry/{id}` endpoints."""

    async def _get_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        data = await self._get(f"/auctions/entry/{auction_id}", api_version="v1")
        return AuctionEntryExpanded._from_data(data["auction"])

    async def _get_bids_by_id(self, auction_id: str) -> list[Bid]:
        data = await self._get(
            f"/auctions/entry/{auction_id}/bids",
            api_version="v1",
        )
        return [
            Bid(
                id=bid["id"],
                auction=bid["auction"],
                user=bid["user"],
                value=bid["value"],
                created=parse_iso_datetime(bid.get("created")),
                updated=parse_iso_datetime(bid.get("updated")),
            )
            for bid in data["bids"]
        ]
