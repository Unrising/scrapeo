import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_country_links() -> dict:
    """
    Récupère tous les pays disponibles sur Numbeo avec leurs liens
    vers la page de coût de la vie.

    Retourne (exemple): 
        dict : {'France' : 'https://www.numbeo.com/cost-of-living/country_result.jsp?country=France'}
    
    """
    # URL de base pour accéder à la liste des pays
    url = "https://www.numbeo.com/cost-of-living/"

    # Pour éviter d'être bloqué
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9"
    }


    # Utilisation de la librairie requests pour récuperer la page html de l'url
    response = requests.get(url, headers=headers)

    # Vérification de la réussite de la requête
    if response.status_code != 200:
        raise Exception(f"Erreur lors du chargement de la page : {response.status_code}")
    
    # On va venir utiliser la librairie BeautifulSoup pour faciliter la lecture de la page html
    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche de la table avec les liens vers les pays
    country_section = soup.find("table", {"class": "related_links"})

    # Vérification qu'on récupère les pays
    if not country_section:
        raise Exception("Impossible de trouver la table des pays")
    
    # On cherche tous les éléments <a> 
    links = country_section.find_all("a")

    # On initialise un dictionnaire vide pour les liens 
    country_links = {}

    # Construction du dictionnaire {pays:liens}
    for link in links:
        country_name = link.text.strip()
        href = link.get("href")
        if href and "country_result.jsp?country=" in href:
            full_url = urljoin("https://www.numbeo.com/cost-of-living/", href)
            country_links[country_name] = full_url
    
    # On retourne le dictionnaire 
    return country_links

