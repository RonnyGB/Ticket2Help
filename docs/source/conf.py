# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'TICKET2HELP'
copyright = '2024, ANA SILVA, RONALD COSTA, DIOGO REGADAS'
author = 'ANA SILVA, RONALD COSTA, DIOGO REGADAS'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'pt'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# -- Django setup ------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))  # Ajuste o caminho conforme necessário
sys.path.insert(1, os.path.abspath('../../tickets'))  # Adicione o diretório do aplicativo tickets
os.environ['DJANGO_SETTINGS_MODULE'] = 'Ticket2Help_P4.settings'
import django
django.setup()
