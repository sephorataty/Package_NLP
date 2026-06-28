"""
Habillage visuel du rapport : injection d'un thème CSS et page de garde.

C'est ce module qui transforme la sortie HTML brute de nbconvert en un
rapport agréable à lire : sommaire en barre latérale fixe, typographie
soignée, tableaux et blocs de code stylés, mise en page responsive.
"""

from __future__ import annotations

from typing import Optional

from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Thème CSS clair, moderne et lisible.
# Les couleurs sont définies via des variables CSS (:root) pour être faciles
# à personnaliser. La mise en page place le sommaire en colonne fixe à gauche.
# ---------------------------------------------------------------------------
_CSS_CLAIR = """
:root {
  --couleur-accent: #4f46e5;        /* indigo : titres, liens, accents */
  --couleur-accent-clair: #eef2ff;
  --couleur-texte: #1f2937;
  --couleur-texte-doux: #6b7280;
  --couleur-fond: #ffffff;
  --couleur-fond-doux: #f9fafb;
  --couleur-bordure: #e5e7eb;
  --largeur-sommaire: 270px;
  --largeur-contenu: 860px;
  --rayon: 8px;
}

html { scroll-behavior: smooth; }

body {
  font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--couleur-texte);
  background: var(--couleur-fond);
  line-height: 1.65;
  margin: 0;
  padding: 0;
  font-size: 16px;
}

/* ---- Sommaire en barre latérale fixe ---- */
#toc {
  position: fixed;
  top: 0;
  left: 0;
  width: var(--largeur-sommaire);
  height: 100vh;
  overflow-y: auto;
  background: var(--couleur-fond-doux);
  border-right: 1px solid var(--couleur-bordure);
  padding: 28px 20px;
  box-sizing: border-box;
}
#toc .toc-titre {
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--couleur-texte-doux);
  margin: 0 0 14px 0;
  border: none;
  padding: 0;
}
#toc ul { list-style: none; margin: 0; padding-left: 14px; }
#toc > ul { padding-left: 0; }
#toc li { margin: 2px 0; }
#toc a {
  color: var(--couleur-texte);
  text-decoration: none;
  font-size: 0.9rem;
  display: block;
  padding: 4px 8px;
  border-radius: 6px;
  border-left: 2px solid transparent;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
#toc a:hover {
  background: var(--couleur-accent-clair);
  color: var(--couleur-accent);
  border-left-color: var(--couleur-accent);
}

/* ---- Zone de contenu (décalée à droite du sommaire) ---- */
body > *:not(#toc) {
  max-width: var(--largeur-contenu);
}
/* nbconvert enveloppe le contenu dans .container ou #notebook : on le décale */
.container, #notebook, #notebook-container, body {
  margin-left: var(--largeur-sommaire);
}
#notebook-container {
  max-width: var(--largeur-contenu);
  margin-left: auto;
  margin-right: auto;
  padding: 48px 40px 80px 40px;
  box-shadow: none;
  border: none;
  background: transparent;
}

/* ---- Page de garde ---- */
.rapport-cover {
  margin: 0 0 56px 0;
  padding: 0 0 32px 0;
  border-bottom: 3px solid var(--couleur-accent);
}
.rapport-cover .titre {
  font-size: 2.4rem;
  font-weight: 700;
  color: var(--couleur-texte);
  margin: 0 0 8px 0;
  line-height: 1.2;
}
.rapport-cover .sous-titre {
  font-size: 1.15rem;
  color: var(--couleur-texte-doux);
  margin: 0 0 20px 0;
}
.rapport-cover .meta {
  font-size: 0.95rem;
  color: var(--couleur-texte-doux);
}
.rapport-cover .meta span { margin-right: 18px; }

/* ---- Titres ---- */
h1, h2, h3, h4 {
  color: var(--couleur-texte);
  font-weight: 650;
  line-height: 1.3;
  scroll-margin-top: 20px;  /* évite que l'ancre passe sous le bord haut */
}
h1 { font-size: 1.9rem; margin-top: 2.2em; }
h2 {
  font-size: 1.45rem;
  margin-top: 2em;
  padding-bottom: 0.3em;
  border-bottom: 1px solid var(--couleur-bordure);
}
h3 { font-size: 1.18rem; margin-top: 1.6em; }

/* ---- Liens ---- */
a { color: var(--couleur-accent); }

/* ---- Blocs de code et sorties ---- */
pre, code {
  font-family: "SFMono-Regular", "Cascadia Code", Consolas, monospace;
  font-size: 0.875em;
}
div.output_area pre, .jp-RenderedText pre {
  background: var(--couleur-fond-doux);
  border: 1px solid var(--couleur-bordure);
  border-radius: var(--rayon);
  padding: 14px 16px;
  overflow-x: auto;
}
code {
  background: var(--couleur-accent-clair);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--couleur-accent);
}
pre code { background: none; padding: 0; color: inherit; }

/* ---- Tableaux ---- */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 18px 0;
  font-size: 0.9rem;
}
table th {
  background: var(--couleur-accent);
  color: #fff;
  text-align: left;
  padding: 10px 12px;
  font-weight: 600;
}
table td {
  padding: 9px 12px;
  border-top: 1px solid var(--couleur-bordure);
}
table tr:nth-child(even) td { background: var(--couleur-fond-doux); }

/* ---- Images et graphiques ---- */
img, .output_png img, .jp-OutputArea img { max-width: 100%; height: auto; }

/* ---- Responsive : sous 1100px le sommaire passe en haut ---- */
@media (max-width: 1100px) {
  #toc {
    position: static;
    width: auto;
    height: auto;
    border-right: none;
    border-bottom: 1px solid var(--couleur-bordure);
  }
  .container, #notebook, #notebook-container, body { margin-left: 0; }
  #notebook-container { padding: 28px 20px 60px 20px; }
}

/* ---- Impression PDF ---- */
@media print {
  #toc { display: none; }
  .container, #notebook, #notebook-container, body { margin-left: 0; }
}
"""


def inject_css(html_content: str, theme: str = "clair") -> str:
    """
    Injecte le thème CSS dans la balise <head> du rapport.

    Paramètres
    ----------
    html_content : str
        Le contenu HTML.
    theme : str, défaut "clair"
        Nom du thème. Seul "clair" est fourni pour l'instant.

    Retour
    ------
    str
        Le HTML avec le style injecté.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    css = _CSS_CLAIR  # un seul thème pour l'instant ; extensible plus tard
    style_tag = soup.new_tag("style")
    style_tag.string = css

    head = soup.head
    if head is None:
        # Si le HTML n'a pas de <head>, on en crée un.
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            soup.insert(0, head)
    head.append(style_tag)

    return str(soup)


def add_cover(html_content: str,
              titre: str,
              sous_titre: Optional[str] = None,
              auteur: Optional[str] = None,
              date: Optional[str] = None) -> str:
    """
    Ajoute une page de garde (titre, sous-titre, auteur, date) en haut du
    rapport, juste après le sommaire.

    Paramètres
    ----------
    titre : str
        Titre principal du rapport.
    sous_titre : str, optionnel
        Sous-titre affiché sous le titre.
    auteur : str, optionnel
        Nom de l'auteur.
    date : str, optionnel
        Date du rapport (texte libre, ex. "Juin 2026").

    Retour
    ------
    str
        Le HTML avec la page de garde ajoutée.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    cover = soup.new_tag("div", **{"class": "rapport-cover"})

    h = soup.new_tag("div", **{"class": "titre"})
    h.string = titre
    cover.append(h)

    if sous_titre:
        st = soup.new_tag("div", **{"class": "sous-titre"})
        st.string = sous_titre
        cover.append(st)

    if auteur or date:
        meta = soup.new_tag("div", **{"class": "meta"})
        if auteur:
            sa = soup.new_tag("span")
            sa.string = f"Auteur : {auteur}"
            meta.append(sa)
        if date:
            sd = soup.new_tag("span")
            sd.string = f"Date : {date}"
            meta.append(sd)
        cover.append(meta)

    # On insère la page de garde dans le conteneur de contenu si possible,
    # sinon directement dans le body.
    cible = (soup.find(id="notebook-container")
             or soup.find(class_="container")
             or soup.body)
    if cible is not None:
        cible.insert(0, cover)

    return str(soup)
