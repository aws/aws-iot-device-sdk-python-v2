# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from datetime import datetime

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'AWS IoT Device SDK v2 for Python'
copyright = '%s, Amazon Web Services, Inc' % datetime.now().year
author = 'Amazon Web Services, Inc'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx', # for linking external docs (ex: aws-crt-python)
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# For cross-linking to types from other libraries
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'awscrt': ('https://awslabs.github.io/aws-crt-python', None),
}

# -- Options for HTML output -------------------------------------------------

autoclass_content = "both"
#autodoc_default_flags = ['show-inheritance','members','undoc-members']
autodoc_default_options = {
    "show-inheritance": True,
    "members": True,
    "member-order": "bysource",
}
autodoc_typehints = 'description'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

