"""
Tokenisation avec SpaCy (plus précise pour le français).

SpaCy est plus lent que NLTK : il est conseillé de l'appliquer sur des
extraits plutôt que sur un roman entier. Le modèle français est chargé
paresseusement (lazy loading) et mis en cache pour éviter de le recharger
à chaque appel.
"""

from __future__ import annotations

from typing import List, Optional

# Nom du modèle français léger de SpaCy.
MODELE_FR_DEFAUT = "fr_core_news_sm"

# Cache interne du modèle chargé (évite de le recharger à chaque appel).
_nlp_cache = {}


def charger_nlp(modele: str = MODELE_FR_DEFAUT):
    """
    Charge (et met en cache) un modèle SpaCy.

    Paramètres
    ----------
    modele : str, défaut "fr_core_news_sm"
        Le nom du modèle SpaCy à charger.

    Retour
    ------
    spacy.language.Language
        L'objet `nlp` prêt à l'emploi.

    Lève
    ----
    OSError
        Si le modèle n'est pas installé. Message d'aide explicite fourni :
        il faut alors lancer `python -m spacy download fr_core_news_sm`.
    """
    # Si le modèle est déjà chargé, on renvoie la version en cache.
    if modele in _nlp_cache:
        return _nlp_cache[modele]

    import spacy  # import local : SpaCy n'est requis que pour ce module

    try:
        nlp = spacy.load(modele)
    except OSError as exc:
        raise OSError(
            f"Le modèle SpaCy '{modele}' n'est pas installé.\n"
            f"Installez-le avec :\n"
            f"    python -m spacy download {modele}"
        ) from exc

    _nlp_cache[modele] = nlp
    return nlp


def spacy_tokens(texte: str, nlp=None,
                modele: str = MODELE_FR_DEFAUT,
                ignorer_espaces: bool = True) -> List[str]:
    """
    Tokenise un texte avec SpaCy.

    Paramètres
    ----------
    texte : str
        Le texte (idéalement un extrait) à tokeniser.
    nlp : spacy.language.Language, optionnel
        Un objet `nlp` déjà chargé. Si None, le modèle est chargé
        automatiquement via `charger_nlp`.
    modele : str, défaut "fr_core_news_sm"
        Modèle à charger si `nlp` n'est pas fourni.
    ignorer_espaces : bool, défaut True
        Si True, exclut les tokens composés uniquement d'espaces.

    Retour
    ------
    List[str]
        La liste des tokens (texte de chaque token).
    """
    if nlp is None:
        nlp = charger_nlp(modele)

    doc = nlp(texte)
    # token.is_space est True pour les tokens d'espacement (sauts de ligne...)
    if ignorer_espaces:
        return [token.text for token in doc if not token.is_space]
    return [token.text for token in doc]
