"""
Génération d'un sommaire (table des matières) à partir des titres du rapport.

Réécriture robuste de la logique d'imbrication : le sommaire reste
correctement structuré même quand on saute des niveaux (par ex. un h1
suivi directement d'un h3) ou qu'on remonte de plusieurs niveaux d'un coup.
"""

from __future__ import annotations

import re
from typing import List, Tuple

from bs4 import BeautifulSoup


def _slugify(texte: str) -> str:
    """
    Transforme un titre en identifiant utilisable dans une URL (#ancre).

    Exemple : "1. Analyse des données" -> "1-analyse-des-donnees"
    """
    texte = texte.lower().strip()
    # Remplace tout ce qui n'est pas lettre/chiffre par un tiret
    texte = re.sub(r"[^\w\s-]", "", texte)
    texte = re.sub(r"[\s_-]+", "-", texte)
    return texte.strip("-") or "section"


def _render_toc(entries: List[Tuple[int, str, str]]) -> str:
    """
    Construit le HTML d'une liste imbriquée <ul>/<li> à partir d'une liste
    plate de titres (niveau, texte, identifiant).

    L'algorithme suit le niveau courant : il ouvre des <ul> quand on
    descend, en ferme quand on remonte, et ferme proprement chaque <li>.
    """
    if not entries:
        return ""

    html: List[str] = []
    depth = 0          # nombre de <ul> actuellement ouverts
    prev = None        # niveau du titre précédent

    for level, text, hid in entries:
        lien = f'<li><a href="#{hid}">{text}</a>'
        if prev is None:
            html.append("<ul>")
            depth += 1
            html.append(lien)
        elif level > prev:
            # On descend : ouvrir autant de <ul> que de niveaux franchis
            for _ in range(level - prev):
                html.append("<ul>")
                depth += 1
            html.append(lien)
        elif level == prev:
            # Même niveau : fermer le <li> précédent avant d'ouvrir le suivant
            html.append("</li>")
            html.append(lien)
        else:
            # On remonte : fermer le <li> courant puis les <ul> excédentaires
            html.append("</li>")
            for _ in range(prev - level):
                html.append("</ul>")
                depth -= 1
                html.append("</li>")
            html.append(lien)
        prev = level

    # Fermeture finale : le dernier <li> puis tous les <ul> encore ouverts
    html.append("</li>")
    while depth > 0:
        html.append("</ul>")
        depth -= 1
        if depth > 0:
            html.append("</li>")

    return "".join(html)


def add_toc(html_content: str, niveau_min: int = 1, niveau_max: int = 3) -> str:
    """
    Ajoute un sommaire hiérarchisé au contenu HTML.

    Le sommaire est inséré en début de <body> dans un <div id="toc">,
    et chaque titre du document reçoit un identifiant pour permettre la
    navigation par ancres.

    Paramètres
    ----------
    html_content : str
        Le contenu HTML du rapport.
    niveau_min : int, défaut 1
        Niveau de titre le plus haut à inclure (1 = h1).
    niveau_max : int, défaut 3
        Niveau de titre le plus bas à inclure (3 = h3). Au-delà, les
        titres ne figurent pas dans le sommaire (rapport plus lisible).

    Retour
    ------
    str
        Le HTML avec le sommaire ajouté.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    balises = [f"h{i}" for i in range(niveau_min, niveau_max + 1)]
    headers = soup.find_all(balises)
    if not headers:
        return html_content

    # 1) Attribuer un identifiant unique à chaque titre
    identifiants_utilises: dict[str, int] = {}
    entries: List[Tuple[int, str, str]] = []

    for header in headers:
        # On retire le symbole d'ancre "¶" ajouté par nbconvert
        texte = header.get_text().replace("¶", "").strip()
        if not texte:
            continue

        base = _slugify(texte)
        # Gestion des doublons : "titre", "titre-1", "titre-2"...
        n = identifiants_utilises.get(base, 0)
        hid = base if n == 0 else f"{base}-{n}"
        identifiants_utilises[base] = n + 1

        header["id"] = hid
        niveau = int(header.name[1])  # 'h2' -> 2
        entries.append((niveau, texte, hid))

    # 2) Construire le HTML du sommaire
    toc_html = (
        '<nav id="toc" aria-label="Sommaire">'
        '<h2 class="toc-titre">Sommaire</h2>'
        + _render_toc(entries)
        + "</nav>"
    )

    # 3) Insérer le sommaire au tout début du <body>
    body = soup.body
    if body:
        body.insert(0, BeautifulSoup(toc_html, "html.parser"))

    return str(soup)
