"""
Conversion d'un notebook Jupyter en rapport HTML soigné.

Le notebook est exécuté (les graphiques Plotly interactifs sont conservés),
puis exporté en HTML, nettoyé, doté d'un sommaire, d'une page de garde et
d'un thème CSS.
"""

from __future__ import annotations

import asyncio
import os
import platform
from typing import Optional

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

from .cleaning import remove_html_comments
from .styling import add_cover, inject_css
from .toc import add_toc

# Sous Windows, évite l'avertissement "Proactor event loop..." lié à asyncio
# au moment d'exécuter le notebook.
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def notebook_to_html(
    notebook_path: str,
    output_directory: str = ".",
    output_name: Optional[str] = None,
    *,
    execute: bool = True,
    hide_code: bool = True,
    add_table_of_contents: bool = True,
    toc_max_level: int = 3,
    titre: Optional[str] = None,
    sous_titre: Optional[str] = None,
    auteur: Optional[str] = None,
    date: Optional[str] = None,
    theme: str = "clair",
    timeout: int = -1,
    allow_errors: bool = False,
) -> str:
    """
    Convertit un notebook Jupyter (.ipynb) en rapport HTML stylé.

    Paramètres
    ----------
    notebook_path : str
        Chemin du notebook source.
    output_directory : str, défaut "."
        Dossier où écrire le HTML.
    output_name : str, optionnel
        Nom du fichier de sortie (sans extension). Par défaut, le nom du
        notebook.
    execute : bool, défaut True
        Exécuter le notebook avant export (pour régénérer les sorties).
        Mettre False si le notebook est déjà exécuté et que vous voulez
        juste l'habiller.
    hide_code : bool, défaut True
        Masquer les cellules de code et les invites In[]/Out[] pour un
        rapport orienté lecture.
    add_table_of_contents : bool, défaut True
        Ajouter le sommaire latéral.
    toc_max_level : int, défaut 3
        Niveau de titre le plus bas inclus dans le sommaire.
    titre, sous_titre, auteur, date : str, optionnels
        Informations de la page de garde. Si `titre` est None, aucune page
        de garde n'est ajoutée.
    theme : str, défaut "clair"
        Thème visuel.
    timeout : int, défaut -1
        Délai max d'exécution d'une cellule en secondes (-1 = illimité).
    allow_errors : bool, défaut False
        Continuer l'exécution même si une cellule lève une erreur.

    Retour
    ------
    str
        Chemin du fichier HTML généré.
    """
    # 1) Charger le notebook
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # 2) Exécuter le notebook si demandé
    if execute:
        executor = ExecutePreprocessor(timeout=timeout, allow_errors=allow_errors)
        # IMPORTANT : on exécute le notebook DANS son propre dossier, pour que
        # les chemins relatifs (lecture de fichiers, images...) fonctionnent.
        dossier_notebook = os.path.dirname(os.path.abspath(notebook_path))
        executor.preprocess(notebook, {"metadata": {"path": dossier_notebook}})

    # 3) Exporter en HTML
    html_exporter = HTMLExporter(template_name="classic")
    if hide_code:
        html_exporter.exclude_input = True          # masque le code
        html_exporter.exclude_input_prompt = True   # masque "In[x]"
        html_exporter.exclude_output_prompt = True  # masque "Out[x]"
    # On ne masque JAMAIS les sorties, sinon les graphiques disparaissent.

    resources = {"embed_widgets": True}  # embarque les widgets interactifs
    body, _ = html_exporter.from_notebook_node(notebook, resources=resources)

    # 4) Nettoyer
    body = remove_html_comments(body)

    # 5) Sommaire
    if add_table_of_contents:
        body = add_toc(body, niveau_max=toc_max_level)

    # 6) Thème CSS
    body = inject_css(body, theme=theme)

    # 7) Page de garde (seulement si un titre est fourni)
    if titre:
        body = add_cover(body, titre=titre, sous_titre=sous_titre,
                         auteur=auteur, date=date)

    # 8) Écrire le fichier final
    if output_name is None:
        output_name = os.path.splitext(os.path.basename(notebook_path))[0]
    os.makedirs(output_directory, exist_ok=True)
    html_file_path = os.path.join(output_directory, f"{output_name}.html")

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(body)

    return html_file_path


# Alias de compatibilité avec l'ancien nom de fonction.
def notebook_to_html_plotly(notebook_path, output_directory=".",
                            notebook_name=None):
    """
    Ancienne signature conservée pour compatibilité. Préférez
    `notebook_to_html` pour accéder à toutes les options (page de garde,
    thème, sommaire configurable...).
    """
    return notebook_to_html(
        notebook_path,
        output_directory=output_directory,
        output_name=notebook_name,
    )
