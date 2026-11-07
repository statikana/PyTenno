# PyTenno

[![PyPI version](https://img.shields.io/pypi/v/pytenno.svg)](https://pypi.org/project/pytenno/)
[![Python versions](https://img.shields.io/pypi/pyversions/pytenno.svg)](https://pypi.org/project/pytenno/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**PyTenno** is a modern, fully typed, asynchronous Python wrapper for the **[warframe.market v2 API](https://api.warframe.market/v2)** built on `aiohttp`.

---

## Features

- **Warframe.market v2 Native** Covers all current endpoints (`/v2/items`, `/v2/item/{slug}`, `/v2/item/{slug}/set`, `/v2/orders/item/{slug}`, `/v2/orders/item/{slug}/top`, `/v2/orders/user/{slug}`, `/v2/orders/my`, `/v2/order`, `/v2/riven/*`, `/v2/lich/*`, `/v2/sister/*`, `/v2/user/*`, `/v2/me`, `/v2/locations`, `/v2/missions`, `/v2/npcs`, `/v2/achievements`, `/v2/versions`).
- **Async Context Manager** `async with PyTenno() as tenno:`.
- **Rich Typed Dataclasses** Every response is deserialized into IDE-friendly Python dataclasses with localized `i18n` fields and convenient properties (`.name`, `.slug`, `.icon`, `.wiki_link`, plus backward-compatible `.url_name` and `.item_name` aliases).
- **Crossplay & Multi-Platform Support** Supports `pc`, `ps4`, `xbox`, `switch`, and `mobile` with configurable `Crossplay` and `Language` headers.

---

## Installation

Install the latest release from PyPI:

```bash
pip install -U pytenno
```

Or install the latest development version directly from GitHub:

```bash
pip install git+https://github.com/statikana/pytenno.git
```

---

## Quickstart

### 1. Fetching Item Details, Sets & Top Online Orders

```python
import asyncio
from pytenno import PyTenno, Language, Platform


async def main() -> None:
    async with PyTenno(
        default_language=Language.en,
        default_platform=Platform.pc,
        default_crossplay=True,
    ) as tenno:
        # Fetch full metadata for an item
        item = await tenno.items.get_item("nikana_prime_set")
        print(f"{item.name} | Ducats: {item.ducats} | Mastery Rank: {item.req_mastery_rank} | Tax: {item.trading_tax}")

        # Fetch all parts belonging to an item's set
        item_set = await tenno.items.get_item_set("nikana_prime_blueprint")
        print("Set parts:", [part.name for part in item_set.items])

        # Fetch the top 5 online buy and top 5 online sell orders
        top = await tenno.items.get_top_orders("nikana_prime_set")
        print("\nTop 5 Online Sell Orders:")
        for order in top.sell:
            print(f"  {order.user.ingame_name} ({order.user.status.value}): {order.platinum}p (x{order.quantity})")


asyncio.run(main())
```

### 2. Filtering Top Orders by Mod Rank, Relic Subtype, or Ayatan Stars

```python
import asyncio
from pytenno import PyTenno, Subtype


async def main() -> None:
    async with PyTenno() as tenno:
        # Top orders for a Rank 10 Blind Rage
        maxed_blind_rage = await tenno.items.get_top_orders("blind_rage", rank=10)
        for order in maxed_blind_rage.sell:
            print(f"Rank {order.rank} Blind Rage: {order.platinum}p by {order.user.ingame_name}")

        # Top orders for a fully socketed Ayatan Anasa Sculpture
        anasa = await tenno.items.get_top_orders(
            "ayatan_anasa_sculpture",
            amber_stars=2,
            cyan_stars=2,
        )
        for order in anasa.sell:
            print(f"Socketed Anasa: {order.platinum}p by {order.user.ingame_name}")


asyncio.run(main())
```

### 3. Riven Weapons, Kuva Liches & Sisters of Parvos

```python
import asyncio
from pytenno import PyTenno


async def main() -> None:
    async with PyTenno() as tenno:
        # Riven weapons & attributes
        braton = await tenno.rivens.get_weapon("braton")
        print(f"{braton.name} Riven Disposition: {braton.disposition}")

        attributes = await tenno.rivens.get_attributes()
        print(f"Loaded {len(attributes)} Riven attributes")

        # Kuva Lich & Sister of Parvos manifests
        lich_weapons = await tenno.liches.get_weapons()
        sister_weapons = await tenno.sisters.get_weapons()
        print(f"Kuva weapons: {len(lich_weapons)} | Tenet weapons: {len(sister_weapons)}")

        # Search live Riven auctions
        auctions = await tenno.auctions.find_riven_auctions(weapon_url_name="braton")
        for auction in auctions[:3]:
            print(f"Riven '{auction.item.name}' by {auction.owner.ingame_name} — start: {auction.starting_price}p")


asyncio.run(main())
```

### 4. Authenticated Order Management (`POST / PATCH / DELETE /v2/order`)

```python
import asyncio
from pytenno import PyTenno, OrderType


async def main() -> None:
    async with PyTenno(token="YOUR_JWT_OR_BEARER_TOKEN") as tenno:
        # Get current authenticated user (/v2/me)
        me = await tenno.profile.get_me()
        print(f"Logged in as {me.ingame_name} (Reputation: {me.reputation})")

        # Create a new sell order (/v2/order)
        order = await tenno.orders.create_order(
            item_id="56c3bbfc5d2f0202da32e943",  # Nikana Prime Set
            order_type=OrderType.sell,
            platinum=65,
            quantity=2,
            visible=True,
        )
        print("Created order:", order.id)

        # Update the order price (/v2/order/{id})
        updated = await tenno.orders.update_order(order.id, platinum=60, quantity=1)
        print("Updated price:", updated.platinum)

        # Delete the order (/v2/order/{id})
        await tenno.orders.delete_order(order.id)


asyncio.run(main())
```

---

## Client Interfaces Overview

| Interface | Attribute on `PyTenno` | Description |
| :--- | :--- | :--- |
| **`Items`** | `tenno.items` | Fetch all items (`get_all`), single item details (`get_item`), item sets (`get_item_set`), all item orders (`get_orders`), and top 5 buy/sell orders (`get_top_orders`). |
| **`Profile` / `Orders`** | `tenno.profile`, `tenno.orders`, `tenno.users` | Fetch user profiles (`get_user`, `get_user_by_id`, `get_me`), user orders (`get_orders`, `get_my_orders`, `get_recent_orders`), and create/update/close/delete orders (`create_order`, `update_order`, `close_order`, `delete_order`). |
| **`Rivens`** | `tenno.rivens` | Fetch Riven weapons (`get_weapons`, `get_weapon`) and Riven stat attributes (`get_attributes`). |
| **`Liches`** | `tenno.liches` | Fetch Kuva Lich weapons (`get_weapons`, `get_weapon`), ephemeras (`get_ephemeras`, `get_ephemera`), and quirks (`get_quirks`, `get_quirk`). |
| **`Sisters`** | `tenno.sisters` | Fetch Sister of Parvos Tenet weapons (`get_weapons`, `get_weapon`), ephemeras (`get_ephemeras`, `get_ephemera`), and quirks (`get_quirks`, `get_quirk`). |
| **`Misc`** | `tenno.misc` | Fetch server manifest versions (`get_versions`), locations (`get_locations`), missions (`get_missions`), NPCs (`get_npcs`), achievements (`get_achievements`), and dashboard showcase (`get_dashboard_showcase`). |
| **`Auctions`** | `tenno.auctions`, `tenno.auction_entries` | Search and create Riven, Kuva Lich, and Sister of Parvos auctions (`find_riven_auctions`, `find_lich_auctions`, `find_sister_auctions`, `get_by_id`, `get_bids_by_id`). |
| **`Auth`** | `tenno.auth` | Sign in (`login`), sign out (`signout`), or request password recovery (`restore`). |
