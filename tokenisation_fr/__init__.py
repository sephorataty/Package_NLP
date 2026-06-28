"""
tokenisation_fr
===============

Boîte à outils de tokenisation pour le texte français, regroupant :

- la tokenisation par mots (NLTK) et les statistiques lexicales ;
- la tokenisation en phrases (NLTK) et leurs statistiques ;
- la tokenisation avec SpaCy (plus précise pour le français) ;
- la génération de n-grammes (bigrammes, trigrammes, n-grammes).

Exemple rapide
--------------
>>> from tokenisation_fr import word_tokens, lexical_stats
>>> tokens = word_tokens("Bonjour le monde. Bonjour à tous !")
>>> lexical_stats(tokens)["total"]
9
"""

# On remonte les fonctions des sous-modules au niveau du package
# pour que l'utilisateur puisse écrire :
#     from tokenisation_fr import word_tokens
# plutôt que :
#     from tokenisation_fr.nltk_tokenizer import word_tokens

from .nltk_tokenizer import (
    word_tokens,
    lexical_stats,
    afficher_resume,
)
from .sentence_tokenizer import (
    sentence_tokens,
    sentence_stats,
    afficher_resume_phrases,
)
from .spacy_tokenizer import (
    spacy_tokens,
    charger_nlp,
    MODELE_FR_DEFAUT,
)
from .ngrams import (
    get_bigrams,
    get_trigrams,
    get_ngrams,
)

__version__ = "0.1.0"

# __all__ définit l'API publique (ce qui est importé via `from ... import *`)
__all__ = [
    # mots
    "word_tokens",
    "lexical_stats",
    "afficher_resume",
    # phrases
    "sentence_tokens",
    "sentence_stats",
    "afficher_resume_phrases",
    # spacy
    "spacy_tokens",
    "charger_nlp",
    "MODELE_FR_DEFAUT",
    # n-grammes
    "get_bigrams",
    "get_trigrams",
    "get_ngrams",
    # méta
    "__version__",
]
