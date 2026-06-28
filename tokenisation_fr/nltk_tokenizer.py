"""
Tokenisation par mots et statistiques lexicales avec NLTK.

Ce module enveloppe `nltk.tokenize.word_tokenize` dans des fonctions
réutilisables et ajoute le calcul des statistiques lexicales
(nombre de tokens, taille du vocabulaire, richesse lexicale).
"""

from __future__ import annotations

from typing import Dict, List

import nltk
from nltk.tokenize import word_tokenize


def _ensure_nltk_data() -> None:
    """
    S'assure que les ressources NLTK nécessaires à la tokenisation
    sont présentes ; les télécharge silencieusement si besoin.

    Appelée automatiquement par les fonctions de ce module, l'utilisateur
    n'a donc rien à télécharger manuellement avant le premier appel.
    """
    # Selon la version de NLTK, le tokenizer s'appuie sur 'punkt'
    # et/ou 'punkt_tab'. On tente les deux sans planter si l'un manque.
    for ressource in ("punkt", "punkt_tab"):
        try:
            nltk.data.find(f"tokenizers/{ressource}")
        except LookupError:
            try:
                nltk.download(ressource, quiet=True)
            except Exception:
                # 'punkt_tab' n'existe pas sur les anciennes versions de NLTK :
                # on ignore l'échec tant que 'punkt' est disponible.
                pass


def word_tokens(texte: str, langue: str = "french") -> List[str]:
    """
    Découpe un texte en tokens (mots, ponctuation...).

    Paramètres
    ----------
    texte : str
        Le texte à tokeniser (par exemple un roman déjà nettoyé).
    langue : str, défaut "french"
        La langue passée à NLTK pour gérer les règles propres à la langue.

    Retour
    ------
    List[str]
        La liste ordonnée des tokens.
    """
    _ensure_nltk_data()
    return word_tokenize(texte, language=langue)


def lexical_stats(tokens: List[str]) -> Dict[str, float]:
    """
    Calcule les statistiques lexicales de base d'une liste de tokens.

    Paramètres
    ----------
    tokens : List[str]
        La liste de tokens (issue de `word_tokens`, par exemple).

    Retour
    ------
    Dict[str, float]
        Un dictionnaire contenant :
        - "total"      : nombre total de tokens
        - "vocabulaire": nombre de tokens uniques
        - "richesse"   : richesse lexicale = vocabulaire / total
                         (entre 0 et 1 ; plus c'est élevé, plus le
                          vocabulaire est varié)
    """
    total = len(tokens)
    # set() élimine les doublons -> on obtient les tokens uniques
    vocabulaire = len(set(tokens))
    # Garde-fou : éviter la division par zéro sur un texte vide
    richesse = vocabulaire / total if total else 0.0
    return {"total": total, "vocabulaire": vocabulaire, "richesse": richesse}


def afficher_resume(tokens: List[str], n_premiers: int = 50) -> None:
    """
    Affiche un résumé lisible des statistiques lexicales et les
    premiers tokens. Pratique pour une exploration rapide en notebook.

    Paramètres
    ----------
    tokens : List[str]
        La liste de tokens à résumer.
    n_premiers : int, défaut 50
        Nombre de tokens à afficher en aperçu.
    """
    stats = lexical_stats(tokens)
    print(f"Nombre total de tokens : {stats['total']:,}")
    print(f"Vocabulaire (tokens uniques) : {stats['vocabulaire']:,}")
    print(f"Richesse lexicale : {stats['richesse']:.4f}")
    print(f"\n{n_premiers} premiers tokens :")
    print(tokens[:n_premiers])
