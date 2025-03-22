import os
import pandas as pd

def save_to_gold(df: pd.DataFrame, filename: str):
    """
    Sauvegarde les données nettoyées dans le dossier 'data/3_gold'
    """
    os.makedirs("data/3_gold", exist_ok=True)
    full_path = os.path.join("data/3_gold", filename)
    df.to_csv(full_path, index=False)
    print(f"\nDonnées sauvegardées dans : {full_path}")