import pandas as pd
import re

def clean_cell(val):
    """
    Fonctions pour nettoyer
    """
    if pd.isna(val):
        return 0.0
    if isinstance(val, str):
        val = val.replace(" ", "")  # espace insécable !
        cleaned = re.sub(r"[^\d,.\-]", "", val).replace(",", ".")
        try:
            return float(cleaned)
        except:
            return 0.0
    try:
        return float(val)
    except:
        return 0.0
    
def convert_to_float(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie toutes les colonnes numériques :
    - Supprime les symboles (€)
    - Remplace les virgules par des points
    - Convertit en float

    Retour :
        DataFrame avec valeurs numériques float
    """
    df = df.copy()

    for col in df.columns:
        if col in ["Ville", "Pays"]:
            continue

        df[col] = df[col].apply(clean_cell)

    return df
