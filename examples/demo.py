"""
Démonstration du package generation_rapport.

Lancez :
    python examples/demo.py

Le script attend un notebook nommé `mon_analyse.ipynb` dans le même
dossier (ou modifiez le chemin ci-dessous).
"""

from generation_rapport import notebook_to_html

if __name__ == "__main__":
    chemin = notebook_to_html(
        "mon_analyse.ipynb",          # <-- votre notebook
        output_directory=".",
        output_name="rapport",
        titre="Rapport d'analyse NLP",
        sous_titre="Master 2 — TP1",
        auteur="Uthaï",
        date="Juin 2026",
    )
    print(f"Rapport généré : {chemin}")
