"""
generation_rapport
==================

Génère des rapports HTML soignés à partir de notebooks Jupyter, en
s'appuyant sur nbconvert. Le rapport produit comporte :

- l'exécution du notebook (graphiques Plotly interactifs conservés) ;
- un sommaire hiérarchisé en barre latérale ;
- une page de garde optionnelle (titre, auteur, date) ;
- un thème CSS clair, lisible et responsive.

Exemple rapide
--------------
>>> from generation_rapport import notebook_to_html
>>> notebook_to_html(
...     "mon_analyse.ipynb",
...     titre="Rapport d'analyse NLP",
...     auteur="Uthaï",
...     date="Juin 2026",
... )
"""

from .converter import notebook_to_html, notebook_to_html_plotly
from .toc import add_toc
from .styling import inject_css, add_cover
from .cleaning import remove_html_comments

__version__ = "0.1.0"

__all__ = [
    "notebook_to_html",
    "notebook_to_html_plotly",
    "add_toc",
    "inject_css",
    "add_cover",
    "remove_html_comments",
    "__version__",
]
