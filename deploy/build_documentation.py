"""Script to generate Sphinx .rst documentation files for PyTenno."""

import os

source = os.path.join(".", "pytenno")
output = os.path.join(".", "docs")

ignored_files = [
    "constants.py",
    "conf.py",
]


def iter_py_files(source_dir: str):
    for root, _dirs, files in os.walk(source_dir):
        rel_root = os.path.relpath(root, ".")
        parts = rel_root.split(os.sep)
        if any(p.startswith("_") for p in parts) or "examples" in parts:
            continue
        for file in sorted(files):
            if (
                file.endswith(".py")
                and not file.startswith("_")
                and file not in ignored_files
            ):
                mod_parts = parts + [file.removesuffix(".py")]
                yield ".".join(mod_parts)


module_template = """\
{title}
.. automodule:: {module}
    :inherited-members:
    :members:
"""

index_template = """\
PyTenno Documentation
=====================

**PyTenno** is a modern, fully typed, asynchronous Python wrapper for the
`warframe.market v2 API <https://api.warframe.market/v2>`_, built on top of
``aiohttp``.

Key Features
------------

* **Full Warframe.market v2 API Support** — Covers items, item sets, live & top-5 orders, user profiles, authenticated order creation/updating/closing, Riven weapons & attributes, Kuva Liches, Sisters of Parvos, star chart locations, missions, NPCs, achievements, and auctions.
* **Async Context Manager** — Clean session lifecycle management using ``async with PyTenno() as tenno:``.
* **Typed Dataclasses & Localized i18n** — Responses are parsed into structured dataclasses with convenient properties (``.name``, ``.slug``, ``.icon``, ``.wiki_link``) as well as backward-compatible v1 aliases (``.url_name``, ``.item_name``).
* **Crossplay & Multi-Platform** — Built-in support for ``pc``, ``ps4``, ``xbox``, ``switch``, and ``mobile`` platforms with configurable ``Language`` and ``Crossplay`` headers.

Installation
------------

Install the latest version from PyPI:

.. code-block:: bash

    pip install -U pytenno

Or install directly from GitHub:

.. code-block:: bash

    pip install git+https://github.com/statikana/pytenno.git

Quickstart
----------

Fetching Item Details, Sets & Top Online Orders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from pytenno import PyTenno, Language, Platform

    async def main():
        async with PyTenno(
            default_language=Language.en,
            default_platform=Platform.pc,
            default_crossplay=True,
        ) as tenno:
            # Fetch a single item's full metadata
            item = await tenno.items.get_item("nikana_prime_set")
            print(item.name, "Ducats:", item.ducats, "Tax:", item.trading_tax)

            # Fetch all items belonging to a set
            item_set = await tenno.items.get_item_set("nikana_prime_blueprint")
            for part in item_set.items:
                print("Part:", part.name, part.slug)

            # Fetch the top 5 online buy and top 5 online sell orders
            top = await tenno.items.get_top_orders("nikana_prime_set")
            for order in top.sell:
                print(order.user.ingame_name, order.platinum, "plat")

    asyncio.run(main())

Filtering Top Orders by Mod Rank or Ayatan Stars
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from pytenno import PyTenno

    async def main():
        async with PyTenno() as tenno:
            # Fetch top orders for a maxed (Rank 10) Blind Rage
            top = await tenno.items.get_top_orders("blind_rage", rank=10)
            for order in top.sell:
                print(f"{{order.user.ingame_name}}: {{order.platinum}}p (rank {{order.rank}})")

    asyncio.run(main())

Managing Orders (Authenticated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from pytenno import PyTenno, OrderType

    async def main():
        async with PyTenno(token="YOUR_BEARER_TOKEN") as tenno:
            me = await tenno.profile.get_me()
            print("Signed in as:", me.ingame_name)

            # Create a sell order
            order = await tenno.orders.create_order(
                item_id="56c3bbfc5d2f0202da32e943",
                order_type=OrderType.sell,
                platinum=65,
                quantity=1,
            )

            # Update order price
            await tenno.orders.update_order(order.id, platinum=60)

            # Delete order
            await tenno.orders.delete_order(order.id)

    asyncio.run(main())

Architecture & Interfaces
-------------------------

All API endpoints are grouped logically onto your :class:`~pytenno.client.PyTenno` instance:

* ``tenno.items`` (:class:`~pytenno.interface.items.Items`) — Tradable items, item sets, item orders, and top 5 online orders.
* ``tenno.profile`` / ``tenno.orders`` / ``tenno.users`` (:class:`~pytenno.interface.profile.Profile`) — User profiles, user orders, recent orders, and authenticated order CRUD (`create_order`, `update_order`, `close_order`, `delete_order`).
* ``tenno.rivens`` (:class:`~pytenno.interface.rivens.Rivens`) — Riven weapons and Riven attributes.
* ``tenno.liches`` (:class:`~pytenno.interface.liches.Liches`) — Kuva Lich weapons, ephemeras, and quirks.
* ``tenno.sisters`` (:class:`~pytenno.interface.liches.Sisters`) — Sister of Parvos Tenet weapons, ephemeras, and quirks.
* ``tenno.misc`` (:class:`~pytenno.interface.misc.Misc`) — Manifest versions, locations, missions, NPCs, achievements, and dashboard showcase.
* ``tenno.auctions`` & ``tenno.auction_entries`` (:class:`~pytenno.interface.auctions.Auctions`, :class:`~pytenno.interface.auction_entries.AuctionEntries`) — Riven, Lich, Sister, and Kubrow auctions.
* ``tenno.auth`` (:class:`~pytenno.interface.auth.Auth`) — Account sign-in, sign-out, and password recovery.

API Reference
-------------

.. toctree::
    :maxdepth: 2
    :caption: Core Client & Utilities

    {core_modules}

.. toctree::
    :maxdepth: 2
    :caption: API Interfaces

    {interface_modules}

.. toctree::
    :maxdepth: 2
    :caption: Data Models & Enums

    {model_modules}
"""


def build_files(source_dir: str, output_dir: str) -> None:
    if not os.path.exists(source_dir):
        raise FileNotFoundError(f"Source directory {source_dir} does not exist")

    os.makedirs(output_dir, exist_ok=True)
    generated_files: list[str] = []

    for module in iter_py_files(source_dir):
        print(f"Building {module}")
        path_parts = module.split(".")
        ref_parts = path_parts[1:]
        subpath = os.path.join(output_dir, *ref_parts[:-1])
        os.makedirs(subpath, exist_ok=True)

        title = f"{module}\n{'=' * len(module)}"
        formatted = module_template.format(title=title, module=module)

        rst_path = os.path.join(output_dir, *ref_parts) + ".rst"
        with open(rst_path, "w", encoding="utf-8") as f:
            f.write(formatted)
        generated_files.append("/".join(ref_parts))

    core_modules = [m for m in generated_files if "/" not in m]
    interface_modules = [m for m in generated_files if m.startswith("interface/")]
    model_modules = [m for m in generated_files if m.startswith("models/")]

    print(f"Generated {len(generated_files)} module .rst files")
    print("Building index.rst")
    index_path = os.path.join(output_dir, "index.rst")
    with open(index_path, "w", encoding="utf-8") as out:
        out.write(
            index_template.format(
                core_modules="\n    ".join(core_modules),
                interface_modules="\n    ".join(interface_modules),
                model_modules="\n    ".join(model_modules),
            )
        )

    template_cfg = os.path.join(".", "deploy", "config_template.py")
    target_cfg = os.path.join(output_dir, "conf.py")
    print(f"Copying configuration file [from {template_cfg}]")
    with open(template_cfg, "r", encoding="utf-8") as template:
        with open(target_cfg, "w", encoding="utf-8") as target:
            target.write(template.read())


if __name__ == "__main__":
    build_files(source, output)
