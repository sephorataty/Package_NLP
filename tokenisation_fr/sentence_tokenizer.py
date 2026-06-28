"""
Tokenisation en phrases avec NLTK.

Découpe un texte en phrases et calcule quelques statistiques
(nombre de phrases, longueur moyenne en mots).
"""

from __future__ import annotations

from typing import Dict, List

from nltk.tokenize import sent_tokenize

# On réutilise le helper de téléchargement défini dans le module mots,
# pour ne pas dupliquer la logique de récupération des ressources NLTK.
from .nltk_tokenizer import _ensure_nltk_data


def sentence_tokens(texte: str, langue: str = "french") -> List[str]:
    """
    Découpe un texte en phrases.

    Paramètres
    ----------
    texte : str
        Le texte à découper.
    langue : str, défaut "french"
        La langue passée à NLTK (gère les abréviations, la ponctuation...).

    Retour
    ------
    List[str]
        La liste des phrases.
    """
    _ensure_nltk_data()
    return sent_tokenize(texte, language=langue)


def sentence_stats(phrases: List[str]) -> Dict[str, float]:
    """
    Calcule des statistiques sur une liste de phrases.

    Paramètres
    ----------
    phrases : List[str]
        La liste de phrases (issue de `sentence_tokens`).

    Retour
    ------
    Dict[str, float]
        - "nb_phrases"     : nombre de phrases
        - "longueur_moyenne": nombre moyen de mots par phrase
                              (estimé via un simple split sur les espaces)
    """
    nb_phrases = len(phrases)
    if not nb_phrases:
        return {"nb_phrases": 0, "longueur_moyenne": 0.0}
    # On compte les mots de chaque phrase via split(), puis on moyenne.
    total_mots = sum(len(p.split()) for p in phrases)
    return {
        "nb_phrases": nb_phrases,
        "longueur_moyenne": total_mots / nb_phrases,
    }


def afficher_resume_phrases(phrases: List[str], n_exemples: int = 3,
                            longueur_apercu: int = 100) -> None:
    """
    Affiche un résumé lisible des statistiques de phrases et quelques
    exemples tronqués.

    Paramètres
    ----------
    phrases : List[str]
        La liste de phrases à résumer.
    n_exemples : int, défaut 3
        Nombre de phrases à montrer en exemple.
    longueur_apercu : int, défaut 100
        Nombre de caractères affichés par phrase d'exemple.
    """
    stats = sentence_stats(phrases)
    print(f"Nombre de phrases : {stats['nb_phrases']}")
    print(f"Longueur moyenne d'une phrase : {stats['longueur_moyenne']:.1f} mots")
    print("\nExemples de phrases :")
    for p in phrases[:n_exemples]:
        print(f"  - {p[:longueur_apercu]}...")
