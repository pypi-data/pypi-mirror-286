"""
Configuration file for the Sphinx documentation builder.

 For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
from unittest.mock import MagicMock
import os


sys.path.insert(0, os.path.abspath("."))

# Ensure master_doc is set to 'index'
master_doc = "index"


class MockArgumentParser(MagicMock):
    """Mock argparse module to fix  'may call exit()' sphinx issue."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parse_args = MagicMock(return_value=None)  # Mock parse_args method


sys.modules["argparse"] = MockArgumentParser()


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "juham"
copyright = "2024, juha meskanen"
author = "juha meskanen"
html_static_path = ["_static"]

# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'src')))


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",  # For support of Google and NumPy style docstrings
    "sphinx_autodoc_typehints",
    "sphinx.ext.autodoc",  # For automatic generation of API documentation from docstrings
    "sphinx.ext.intersphinx",  # For cross-referencing to external documentation
    "sphinx.ext.todo",  # For TODO list management
    "sphinx.ext.viewcode",  # For links to the source code
    "sphinx.ext.autosummary",  # For automatic generation of summary tables of contents
    "sphinx.ext.doctest",  # For running doctests in docstrings
    "sphinx.ext.ifconfig",  # For conditional content based on configuration values
    "sphinx.ext.githubpages",  # For publishing documentation to GitHub Pages
    "sphinx.ext.coverage",  # For measuring documentation coverage
    "sphinx.ext.mathjax",  # For rendering math via MathJax
    "sphinx.ext.imgmath",  # For rendering math via LaTeX and dvipng
    "sphinx.ext.inheritance_diagram",  # UML diagrams,
    "sphinxcontrib.plantuml",  # for UML diagrams
]


# platuml
# Path to the PlantUML jar file
plantuml_jar_path = "../plantuml.jar"
plantuml = f"java -jar {plantuml_jar_path}"

# TODO: FIXME, hard coded workstation specific path
os.environ["PATH"] += os.pathsep + "d:/ProgramFiles/Graphviz/bin/"
graphviz_output_format = "svg"

napoleon_google_docstring = True
napoleon_numpy_docstring = False
autodoc_inherit_docstrings = True
templates_path = ["_templates"]
# exclude_patterns = []
todo_include_todos = True
pygments_style = "sphinx"  # Default syntax highlighting style
highlight_language = "python"  # Default language for code blocks


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

import sphinx_bootstrap_theme

html_theme = "bootstrap"
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add any CSS files here, relative to the static path.
# Example: "css/custom.css"
html_css_files = [
    "juham.css",
]

# Additional theme options
# html_theme_options = {
# your other options here
# }
