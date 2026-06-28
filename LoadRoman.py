class LoadRoman:
    """La classe LoadRoman est responsable du chargement du texte brut du roman "Le Comte de Monte-Cristo" 
        à partir d'un url. Elle lit le contenu du fichier et affiche un aperçu du texte, ainsi que sa taille 
        en caractères.
    """
    
    @staticmethod
    def load_roman(url : str):
        """Charge le texte brut du roman à partir de l'url spécifié. Affiche un aperçu du texte et sa taille en caractères.
        
        Args:
            url (str): L'url du fichier texte du roman sur Project Gutenberg.
        
        returns:
            str: Le texte du roman "Le Comte de Monte-Cristo" sans les métadonnées de Project Gutenberg.
        """
        # Téléchargement
        try:
            import requests
            print(f'Téléchargement du roman depuis {url}...')
            roman = requests.get(url)
            roman.encoding = 'utf-8'
            raw_text = roman.text

            print(f'Téléchargement terminé.')
            print(f'Taille brute : {len(raw_text):,} caractères')
            print(f'Aperçu :\n{raw_text[:300]}')
            
        except Exception as e:
        
            print(f'Erreur lors du téléchargement : {e}')
            return None

        return roman