# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath(".."))
import pytenno

# -- Project information -----------------------------------------------------

project = "PyTenno"
copyright = "2022-2026, ShadowMagic896 (statikana)"
author = "ShadowMagic896"

release = pytenno.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]

# -- Options for Autodoc -----------------------------------------------------

autodoc_member_order = "bysource"
