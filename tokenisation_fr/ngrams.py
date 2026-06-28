"""
Génération de n-grammes (bigrammes, trigrammes, n-grammes génériques).

Un n-gramme est une séquence de n tokens consécutifs. Les n-grammes
servent par exemple à repérer les expressions figées ou à construire
des modèles de langue simples.
"""

from __future__ import annotations

from typing import List, Tuple

from nltk import bigrams, ngrams, trigrams


def get_bigrams(tokens: List[str]) -> List[Tuple[str, str]]:
    """
    Génère les bigrammes (séquences de 2 tokens consécutifs).

    Paramètres
    ----------
    tokens : List[str]
        La liste de tokens en entrée.

    Retour
    ------
    List[Tuple[str, str]]
        La liste des bigrammes sous forme de tuples de 2 éléments.
    """
    return list(bigrams(tokens))


def get_trigrams(tokens: List[str]) -> List[Tuple[str, str, str]]:
    """
    Génère les trigrammes (séquences de 3 tokens consécutifs).

    Paramètres
    ----------
    tokens : List[str]
        La liste de tokens en entrée.

    Retour
    ------
    List[Tuple[str, str, str]]
        La liste des trigrammes sous forme de tuples de 3 éléments.
    """
    return list(trigrams(tokens))


def get_ngrams(tokens: List[str], n: int) -> List[Tuple[str, ...]]:
    """
    Génère les n-grammes pour une valeur de n quelconque.

    Paramètres
    ----------
    tokens : List[str]
        La liste de tokens en entrée.
    n : int
        La taille des séquences (n >= 1). n=2 équivaut aux bigrammes,
        n=3 aux trigrammes, etc.

    Retour
    ------
    List[Tuple[str, ...]]
        La liste des n-grammes sous forme de tuples de n éléments.

    Lève
    ----
    ValueError
        Si n < 1.
    """
    if n < 1:
        raise ValueError("n doit être supérieur ou égal à 1.")
    return list(ngrams(tokens, n))
