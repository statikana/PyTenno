"""CLI entry point for PyTenno (`python -m pytenno`)."""

import argparse
import os

from . import __version__

parser = argparse.ArgumentParser(
    prog="pytenno",
    description="Asynchronous Python wrapper for the Warframe.market v2 API.",
)
parser.add_argument("--version", action="version", version=__version__)
parser.add_argument(
    "--example",
    action="store_true",
    help="Create a quickstart example.py file demonstrating Warframe.market v2 endpoints.",
)

args = parser.parse_args()
if isinstance(args, argparse.Namespace) and args.example:
    location = input(
        "Please enter a directory in which to save the example file:\n  | "
    )
    path = os.path.abspath(location)
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, "example.py")
    example = '''"""Example script demonstrating PyTenno with the Warframe.market v2 API."""

import asyncio
from pytenno import Language, Platform, PyTenno


async def main() -> None:
    async with PyTenno(
        default_language=Language.en,
        default_platform=Platform.pc,
    ) as tenno:
        # 1. Fetch an item and its set parts
        item_set = await tenno.items.get_item_set("mirage_prime_set")
        print(f"Set parts for {item_set.root.name}:")
        for part in item_set.items:
            print(f"  - {part.name} ({part.slug}) | Ducats: {part.ducats}")

        # 2. Fetch the top 5 online sell and buy orders
        top_orders = await tenno.items.get_top_orders("mirage_prime_set")
        print("\\nTop 5 Online Sell Orders:")
        for order in top_orders.sell:
            print(f"  - {order.user.ingame_name}: {order.platinum}p (x{order.quantity})")


if __name__ == "__main__":
    asyncio.run(main())
'''
    with open(path, "w", encoding="utf-8") as f:
        f.write(example)
    print(f"Example file created at {path}.")
