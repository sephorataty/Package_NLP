"""
Nettoyage du HTML généré par nbconvert.

Pour l'instant : suppression des commentaires HTML, qui alourdissent
inutilement le fichier final.
"""

from __future__ import annotations

from bs4 import BeautifulSoup, Comment


def remove_html_comments(html_content: str) -> str:
    """
    Supprime tous les commentaires HTML (<!-- ... -->) du contenu.

    Paramètres
    ----------
    html_content : str
        Le contenu HTML à nettoyer.

    Retour
    ------
    str
        Le HTML sans commentaires.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    # On repère les nœuds de type "commentaire" puis on les retire un à un.
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    return str(soup)
