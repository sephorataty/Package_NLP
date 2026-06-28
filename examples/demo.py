"""
Démonstration du package tokenisation_fr.

Ce script reproduit le déroulé d'origine (mots, SpaCy, phrases, n-grammes)
mais en s'appuyant sur les fonctions du package. Lancez-le avec :

    python examples/demo.py

Remplacez le texte d'exemple par le contenu de votre roman nettoyé
(`roman_clean`) pour l'utiliser sur vos propres données.
"""

from Package_NLP.tokenisation_fr import (
    word_tokens,
    afficher_resume,
    sentence_tokens,
    afficher_resume_phrases,
    get_bigrams,
    get_trigrams,
)

# --- Texte d'exemple (à remplacer par votre roman nettoyé) ---
roman_clean = (
    "Il était une fois, dans un petit village du sud de la France, "
    "un vieux libraire passionné de mots. Chaque matin, il ouvrait sa "
    "boutique avec le même plaisir. Les clients venaient de loin pour "
    "écouter ses histoires et repartaient toujours avec un livre sous le bras. "
) * 50  # on répète pour avoir un texte un peu plus long


# --- 1. Tokenisation par mots ---
print("=" * 60)
print("1. TOKENISATION PAR MOTS (NLTK)")
print("=" * 60)
tokens = word_tokens(roman_clean)
afficher_resume(tokens, n_premiers=50)


# --- 2. Tokenisation SpaCy (optionnelle) ---
print("\n" + "=" * 60)
print("2. TOKENISATION SPACY (extrait)")
print("=" * 60)
extrait_ch1 = roman_clean[:5000]
try:
    from Package_NLP.tokenisation_fr import spacy_tokens

    tokens_spacy = spacy_tokens(extrait_ch1)
    print(f"Tokens NLTK (extrait)  : {len(word_tokens(extrait_ch1))}")
    print(f"Tokens SpaCy (extrait) : {len(tokens_spacy)}")
    print("\n30 premiers tokens SpaCy :")
    print(tokens_spacy[:30])
except OSError as exc:
    # Le modèle SpaCy n'est pas installé : on l'indique sans planter la démo.
    print("SpaCy non disponible :")
    print(exc)


# --- 3. Tokenisation en phrases ---
print("\n" + "=" * 60)
print("3. TOKENISATION EN PHRASES (NLTK)")
print("=" * 60)
phrases = sentence_tokens(roman_clean[:20000])
afficher_resume_phrases(phrases, n_exemples=3)


# --- 4. N-grammes ---
print("\n" + "=" * 60)
print("4. N-GRAMMES")
print("=" * 60)
bi = get_bigrams(tokens[:200])
print("Bigrammes (20 premiers) :")
print(bi[:20])

tri = get_trigrams(tokens[:200])
print("\nTrigrammes (10 premiers) :")
print(tri[:10])
