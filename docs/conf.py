"""Sphinx configuration for mammoth-db."""

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "mammoth-db"
copyright = "2026, malkoG"
author = "malkoG"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- autodoc / autosummary ---------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "member-order": "bysource",
}
autodoc_typehints = "description"
autosummary_generate = True

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_ivar = True

# -- HTML output --------------------------------------------------------------
html_theme = "furo"
html_static_path = ["_static"]
