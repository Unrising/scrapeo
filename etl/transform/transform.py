import pandas as pd
import os
# Import des sous-transformations
from etl.transform.functions.duplicate_transform import remove_duplicates
from etl.transform.functions.interrogation_mark_transform import replace_interrogation_marks
from etl.transform.functions.float_transform import convert_to_float

def run_transform_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applique toutes les étapes de transformation :
    1. Supprimer les doublons
    2. Remplacer les "?" par 0
    3. Convertir les colonnes numériques en float

    Paramètre :
        df : DataFrame brut (niveau bronze)

    Retour :
        DataFrame transformé (niveau silver)
    """
    df = df.copy()
    df = remove_duplicates(df)
    df = replace_interrogation_marks(df, replacement_value=0.0)
    df = convert_to_float(df)
    return df

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

    output_name = input("Nom du fichier de sortie (ex: cleaned_france) : ").strip()
    if not output_name.endswith(".csv"):
        output_name += ".csv"

    output_path = os.path.join("data/2_silver", output_name)

    df_transformed = run_transform_pipeline(df)
    df_transformed.to_csv(output_path, index=False)

    print(f"\nTransformation terminée. Fichier sauvegardé : {output_path}")
    print(df_transformed.head())