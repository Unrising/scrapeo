import os
import pandas as pd
from etl.extract.extract import run_extraction_pipeline
from etl.transform.transform import transform_pipeline
from ml.ml import run_ml

def run_extract():
    print("\n--- Extraction des données ---")
    countries = input("Entrez les pays séparés par une virgule (ex: France,Germany,Italy) : ")
    country_list = [c.strip() for c in countries.split(",") if c.strip()]

    limit_cities = input("Nombre de villes max par pays (laisser vide = illimité) : ")
    limit_cities = int(limit_cities) if limit_cities.strip().isdigit() else None

    filename = input("Nom du fichier de sortie (ex: france_scraping.csv) : ").strip()
    if not filename.endswith(".csv"):
        filename += ".csv"

    save_path = os.path.join("3_data/1_bronze", filename)

    df = run_extraction_pipeline(
        delay_between_request=1,
        country_list=country_list,
        limit_cities=limit_cities
    )

    df.to_csv(save_path, index=False)
    print(f"\nExtraction terminée. Fichier sauvegardé : {save_path}")
    print(df.head())

def run_transform():
    print("\n--- Transformation des données ---")
    bronze_dir = "data/1_bronze"
    files = [f for f in os.listdir(bronze_dir) if f.endswith(".csv")]

    if not files:
        print("Aucun fichier trouvé dans 3_data/1_bronze/")
        return

    print("\nFichiers disponibles à transformer :")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    choice = input("Sélectionne le fichier à transformer (numéro) : ")
    try:
        index = int(choice) - 1
        selected_file = files[index]
    except:
        print("Choix invalide.")
        return

    df = pd.read_csv(os.path.join(bronze_dir, selected_file))

    output_name = input("Nom du fichier de sortie (ex: cleaned_france.csv) : ").strip()
    if not output_name.endswith(".csv"):
        output_name += ".csv"

    output_path = os.path.join("data/2_silver", output_name)

    df_transformed = transform_pipeline(df)
    df_transformed.to_csv(output_path, index=False)

    print(f"\nTransformation terminée. Fichier sauvegardé : {output_path}")
    print(df_transformed.head())

if __name__ == "__main__":
    print("\nQue veux-tu faire ?")
    print("1. Scraper les données (EXTRACT)")
    print("2. Transformer les données (TRANSFORM)")
    print("3. Machine Learning (ML)")
    print("4. Quitter")

    choice = input("Choix [1/2/3/4] : ").strip()

    if choice == "1":
        run_extract()
    elif choice == "2":
        run_transform()
    elif choice == "3":
        run_ml()
    elif choice == "4":
        print("Au revoir !")
    else:
        print("Choix invalide.")
