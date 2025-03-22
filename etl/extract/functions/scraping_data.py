import requests 
from bs4 import BeautifulSoup
import pandas as pd

def try_url(url):
    """
    Tente de charger la page, retourne l'objet response si OK.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9"
    }
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            return r
    except Exception as e:
        print(f"Erreur lors de l'accès à {url} : {e}")
    return None

def scrape_city_data(city_name: str, country_name: str) -> pd.DataFrame:
    """
    Scrape les données de coût de la vie pour une ville donnée.
    Teste plusieurs URLs jusqu’à trouver une qui contient des données.
    """
    base = "https://www.numbeo.com/cost-of-living/in/"
    city_part = city_name.replace(" ", "-")
    country_part = country_name.replace(" ", "-")
    urls = [
        f"{base}{city_part}",               # Ex: /in/Paris
        f"{base}{city_part}-{country_part}" # Ex: /in/Acheres-France
    ]

    final_url = None
    response = None
    soup = None
    table = None

    for url in urls:
        res = try_url(url)
        if res:
            temp_soup = BeautifulSoup(res.text, "html.parser")
            temp_table = temp_soup.find("table", class_=lambda x: x and "data_wide_table" in x)
            if temp_table:
                response = res
                soup = temp_soup
                table = temp_table
                final_url = url
                break  # on garde cette URL
            else:
                print(f"Pas de tableau trouvé dans : {url}")
        else:
            print(f"Échec de requête pour : {url}")

    if not table:
        print(f"Aucun tableau trouvé pour {city_name} ({country_name})")
        return pd.DataFrame()

    # Extraction des données
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            item = cols[0].text.strip()
            value = cols[1].text.strip()
            if value == "?":
                value = None
            data.append({
                "Ville": city_name,
                "Pays": country_name,
                "Catégorie": item,
                "Valeur": value
            })

    df = pd.DataFrame(data)

    # Pivot pour avoir 1 ligne par ville
    df_pivot = df.pivot_table(
        index=["Ville", "Pays"],
        columns="Catégorie",
        values="Valeur",
        aggfunc="first"
    ).reset_index()

    df_pivot.columns.name = None
    print(f"Scraping réussi : {city_name} ({country_name}) depuis {final_url}")
    return df_pivot

# Code de test
if __name__ == "__main__":
    city = "Acheres"
    country = "France"
    df = scrape_city_data(city, country)
    print(df.head())
