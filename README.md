# tokenisation-fr

Boîte à outils de **tokenisation pour le texte français**, pensée pour être réutilisable et publiable. Elle regroupe quatre familles de fonctions :

- **Tokenisation par mots** (NLTK) + statistiques lexicales
- **Tokenisation en phrases** (NLTK) + statistiques
- **Tokenisation avec SpaCy** (plus précise pour le français)
- **Génération de n-grammes** (bigrammes, trigrammes, n-grammes)

## Installation

### Depuis GitHub

```bash
pip install git+https://github.com/<ton-utilisateur>/tokenisation-fr.git
```

### En local (mode développement)

```bash
git clone https://github.com/<ton-utilisateur>/tokenisation-fr.git
cd tokenisation-fr
pip install -e .
```

### Pour utiliser le module SpaCy

SpaCy est une dépendance **optionnelle**. Pour l'activer :

```bash
pip install "tokenisation-fr[spacy]"
python -m spacy download fr_core_news_sm
```

> Les ressources NLTK (`punkt`) sont téléchargées automatiquement au premier appel, rien à faire de ce côté.

## Utilisation

### 1. Tokenisation par mots et statistiques lexicales

```python
from tokenisation_fr import word_tokens, lexical_stats, afficher_resume

tokens = word_tokens(roman_clean)            # langue="french" par défaut
afficher_resume(tokens, n_premiers=50)       # affiche un résumé complet

stats = lexical_stats(tokens)                # ou récupère les chiffres
print(stats["total"], stats["vocabulaire"], stats["richesse"])
```

### 2. Tokenisation avec SpaCy (sur un extrait)

```python
from tokenisation_fr import spacy_tokens, word_tokens

extrait = roman_clean[:5000]
tokens_spacy = spacy_tokens(extrait)         # charge le modèle automatiquement

print("NLTK :", len(word_tokens(extrait)))
print("SpaCy:", len(tokens_spacy))
print(tokens_spacy[:30])
```

Si tu traites plusieurs extraits, charge le modèle une seule fois :

```python
from tokenisation_fr import charger_nlp, spacy_tokens

nlp = charger_nlp()                          # chargé + mis en cache
tokens = spacy_tokens(extrait, nlp=nlp)      # réutilise le même modèle
```

### 3. Tokenisation en phrases

```python
from tokenisation_fr import sentence_tokens, afficher_resume_phrases

phrases = sentence_tokens(roman_clean[:20000])
afficher_resume_phrases(phrases, n_exemples=3)
```

### 4. N-grammes

```python
from tokenisation_fr import get_bigrams, get_trigrams, get_ngrams

bi = get_bigrams(tokens[:200])
tri = get_trigrams(tokens[:200])
quad = get_ngrams(tokens[:200], n=4)         # n-grammes génériques

print(bi[:20])
print(tri[:10])
```

## Structure du projet

```
tokenisation/
├── tokenisation_fr/
│   ├── __init__.py            # API publique du package
│   ├── nltk_tokenizer.py      # mots + statistiques lexicales
│   ├── sentence_tokenizer.py  # phrases + statistiques
│   ├── spacy_tokenizer.py     # tokenisation SpaCy (chargement paresseux)
│   └── ngrams.py              # bigrammes / trigrammes / n-grammes
├── examples/
│   └── demo.py                # script de démonstration
├── pyproject.toml             # configuration du package
├── requirements.txt
└── README.md
```

## Licence

MIT — libre d'utilisation, de modification et de redistribution.
"# Package_NLP" 
