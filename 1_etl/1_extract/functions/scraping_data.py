import requests 
from bs4 import BeautifulSoup
import pandas as pd


def try_url(url):
    """
    On doit essayer deux types d'urls car pour 
    Exemple :
    Paris -> url = https://www.numbeo.com/cost-of-living/in/Paris
    Amiens -> url = https://www.numbeo.com/cost-of-living/in/Amiens-France
    """
    # Pour éviter d'être bloqué 
    headers = {"User-Agent": "Mozilla/5.0"}

    # Utilisation de la librairie requests pour récupérer la page html de l'url
    r = requests.get(url, headers=headers)

    return r if r.status_code == 200 else None

def scrape_city_data(city_url: str, city_name: str, country_name: str) -> pd.DataFrame:
    """
    Scrape les données de coût de la vie pour une ville donnée.

    Paramètres :
        city_url (str) : URL de la page de la ville sur Numbeo
        city_name (str) : Nom de la ville
        country_name (str) : Nom du pays

    Retourne :
        pd.DataFrame : Données extraites sous forme de tableau
    """
    # Construction des deux URLs à tester
    base = "https://www.numbeo.com/cost-of-living/in/"
    city_part = city_name.replace(" ", "-")
    country_part = country_name.replace(" ", "-")
    urls = [
        f"{base}{city_part}",               # ex: /in/Paris
        f"{base}{city_part}-{country_part}" # ex: /in/Amiens-France
    ]

    # Réponse de la requête 
    response = None
    
    # L'url qu'on va garder
    final_url = None

    # On va venir effectuer une boucle pour tester les deux urls 
    for url in urls:
        res = try_url(url)
        if res:
            response = res
            final_url = url
            break
    
    # Si on peut pas scrape la ville on renvoie un dataframe vide
    if not response:
        print(f"Échec du scraping pour {city_name} ({country_name})")
        return pd.DataFrame()

    # On va venir utiliser la librairie BeautifulSoup pour faciliter la lecture de la page html
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouver le tableau principal contenant les données
    table = soup.find("table", {"class": "data_wide_table"})

    # Vérification qu'on récupère les données et sinon on renvoie un dataframe vide
    if not table:
        print(f"Aucun tableau trouvé pour {city_name} ({country_name})")
        return pd.DataFrame()

    # Chaque rangées de données
    rows = table.find_all("tr")

    # On initialise un tableau vide
    data = []

    # Construction du dataframe
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            item = cols[0].text.strip()
            value = cols[1].text.strip()
            data.append({
                "Ville": city_name,
                "Pays": country_name,
                "Catégorie": item,
                "Valeur":value
            })
    
    # On transforme data en dataframe
    df = pd.DataFrame(data)
    
    # Pivot : chaque catégorie devient une colonne
    df_pivot = df.pivot_table(
        index=["Ville", "Pays"],
        columns="Catégorie",
        values="Valeur",
        aggfunc="first"  # En cas de doublons
    ).reset_index()

    df_pivot.columns.name = None

    # Console pour savoir si le scraping à réussi et indiquer l'url 
    print(f"Scraping réussi : {city_name} ({country_name}) depuis {final_url}")

    # On retourne le dataframe
    return df_pivot

# Code de test
if __name__ == "__main__":
    city = "Paris"
    country = "France"
    url = "https://www.numbeo.com/cost-of-living/in/Paris-France"
    df = scrape_city_data(url,city,country)
    print(df.head())
