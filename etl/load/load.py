import os
import pandas as pd
from etl.load.functions.save_to_gold import save_to_gold

def run_load_pipeline():
    """
    Pipeline interactif pour charger un fichier silver,
    sélectionner des colonnes, et sauvegarder en gold.
    """
    silver_dir = "data/2_silver"
    files = [f for f in os.listdir(silver_dir) if f.endswith(".csv")]

    if not files:
        print("Aucun fichier trouvé dans 3_data/2_silver/")
        return

    print("\nFichiers silver disponibles :")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    index = int(input("Choisis un fichier (numéro) : ").strip()) - 1
    selected_file = files[index]
    df = pd.read_csv(os.path.join(silver_dir, selected_file))

    print("\nColonnes disponibles :")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")

    print("\n1. Garder toutes les colonnes")
    print("2. Choisir une plage de colonnes (ex: 5 à 20)")
    choice = input("Ton choix [1/2] : ").strip()

    always_keep = ["Ville", "Pays"]
     
    if choice == "2":
        start = int(input("De (numéro) : ").strip()) - 1
        end = int(input("À (numéro) : ").strip())
        selected_columns = list(df.columns[start:end])

        for col in always_keep:
            if col not in selected_columns:
                selected_columns.insert(0, col)

    else:
        selected_columns = list(df.columns)

    df_selected = df[selected_columns]

    output_name = input("\nNom du fichier gold (ex: gold_clean) : ").strip()
    if not output_name.endswith(".csv"):
        output_name += ".csv"

    save_to_gold(df_selected, output_name)
