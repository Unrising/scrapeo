import os
import time
import pandas as pd
from datetime import datetime

# Importation des fonctions de scraping
from etl.extract.functions.scraping_country import get_country_links
from etl.extract.functions.scraping_cities import get_city_links_from_country
from etl.extract.functions.scraping_data import scrape_city_data

def run_extraction_pipeline(
        country_list: list[str] = None,
        limit_countries: int = None,
        limit_cities: int = None,
        save_path: str = "data/1_bronze",
        delay_between_request: float = 1.0
) -> pd.DataFrame:
    """
    Exécute le pipeline complet d'extraction :
    1. Récupération des pays disponibles
    2. Pour chaque pays, récupération des villes disponibles
    3. Pour chaque ville, scraping des données
    4. Fusion des données et sauvegarde dans un fichier CSV (niveau bronze)

    Paramètres :
        limit_countries (int) : Limite de pays à scraper (None = tous)
        limit_cities (int) : Limite de villes par pays (None = toutes)
        save_path (str) : Chemin de sauvegarde du fichier CSV
        delay_between_requests (float) : Délai (en secondes) entre chaque requête

    Retour :
        pd.DataFrame : Données extraites fusionnées
    """

    # Création du dossier de sauvegarde si inexistant 
    os.makedirs(save_path, exist_ok=True)

    # Étape 1 : récupération des liens vers les pages pays
    print("Récupération de la liste des pays disponibles...")
    country_links = get_country_links()

    if country_list:
        # On garde uniquement les pays spécifiés dans la liste
        country_links = {
            name: url for name, url in country_links.items()
            if name in country_list
    }
    # Limitation éventuelle du nombre de pays
    if limit_countries:
        country_links = dict(list(country_links.items())[:limit_countries])

    # Initialisation de la liste des DataFrames collectés
    all_data = []

    # Parcours de chaque pays
    for country_name, country_url in country_links.items():
        print(f"\nTraitement du pays : {country_name}")
        try:
            # Étape 2 : récupération des villes du pays
            city_links = get_city_links_from_country(country_url)
            if limit_cities:
                city_links = dict(list(city_links.items())[:limit_cities])    
        
        except Exception as e:
            print(f"Erreur lors du scraping des villes pour {country_name} : {e}")
            continue
            
        # Parcours de chaque ville du pays
        for city_name, city_url in city_links.items():
            print(f"Ville en cours : {city_name} + {city_url}")

            try: 
                # Étape 3 : récupération des données de la ville
                df_city = scrape_city_data(city_name, country_name)

                # Si les données sont valides, on les ajoute à la liste
                if not df_city.empty:
                    all_data.append(df_city)
            
            except Exception as e:
                print(f"Erreur lors du scraping de {city_name} avec le lien {city_url} : {e}")
                continue

            # Pause pour éviter de se faire bannir du site
            time.sleep(delay_between_request)

    # Si aucune donnée n'a été collectée
    if not all_data:
        print("Aucune donnée n'a pu être extraite")
        return pd.DataFrame()

    # Fusion de tous les DataFrames collectés
    df_all = pd.concat(all_data, ignore_index = True)

    # Génération d'un nom de fichier avec la date/heure
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"bronze_scraped_{date_str}.csv"
    full_path = os.path.join(save_path, filename)

    # Sauvegarde du fichier CSV
    df_all.to_csv(full_path, index=False)
    print(f"Données sauvegardées dans : {full_path}")

    return df_all

def run_extract():
    print("\n--- Extraction des données ---")
    countries = input("Entrez les pays séparés par une virgule (ex: France,Germany,Italy) : ")
    country_list = [c.strip() for c in countries.split(",") if c.strip()]

    limit_cities = input("Nombre de villes max par pays (laisser vide = illimité) : ")
    limit_cities = int(limit_cities) if limit_cities.strip().isdigit() else None

    filename = input("Nom du fichier de sortie (ex: france_scraping.csv) : ").strip()
    if not filename.endswith(".csv"):
        filename += ".csv"

    save_path = os.path.join("data/1_bronze", filename)

    df = run_extraction_pipeline(
        delay_between_request=1,
        country_list=country_list,
        limit_cities=limit_cities
    )

    df.to_csv(save_path, index=False)
    print(f"\nExtraction terminée. Fichier sauvegardé : {save_path}")
    print(df.head())

