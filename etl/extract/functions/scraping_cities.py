import requests 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_country_name_from_url(country_url: str) -> str:
    """
    Extrait le nom du pays à partir de l'URL (paramètre GET 'country').

    Exemple :
        '...country_result.jsp?country=France' -> 'France'
    """
    query_params = parse_qs(urlparse(country_url).query)
    return query_params.get('country', [''])[0].strip().replace(" ", "-")


def get_city_links_from_country(country_url: str) -> dict:
    """"
    Récupère les liens vers les pages de chaque villes listée dans un pays donné en paramètre. 
    
    Paremètre :
        country_url(str) : URL de la pages pays (exemple : https://www.numbeo.com/cost-of-living/country_result.jsp?country=France')
    
    Retourne (exemple) :
        dict : {'Paris' : 'https://www.numbeo.com/cost-of-living/in/Paris'}
    
    """

    # Pour éviter d'être bloqué
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9"
    }

    # Utilisation de la librairie requests pour récuperer la page html de l'url
    response = requests.get(country_url, headers=headers)

    print(country_url)

    # Vérification de la réussite de la requête
    if response.status_code != 200:
        raise Exception(f"Erreur lors de l'accès à la page du pays : {response.status_code}")
    
    # On va venir utiliser la librairie BeautifulSoup pour faciliter la lecture de la page html
    soup = BeautifulSoup(response.text,"html.parser")

    # Recherche du menu déroulant avec les villes
    select_ville = soup.find("select", {"name":"city","id":"city"})
    
    # Vérification qu'on récupère les villes
    if not select_ville:
        raise Exception("Impossible de trouver la liste des villes dans le menu déroulant.")
    
    # On récupère le nom du pays
    country_name = get_country_name_from_url(country_url)

    # On cherche tous les éléments <option> 
    options = select_ville.find_all("option")

    # On initialise un dictionnaire vide pour les liens 
    city_links = {}

    # Construction du dictionnaire {ville:liens}
    for option in options:
        value = option.get("value")
        if value and "Select city" not in value:
            city_name = value.strip()
            city_url_part = city_name.replace(" ", "-")
            full_url = f"https://www.numbeo.com/cost-of-living/in/{city_url_part}-{country_name}"
            city_links[city_name] = full_url
    
    # On retourne le dictionnaire 
    return city_links

