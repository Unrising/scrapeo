import pandas as pd

# Import des sous-transformations
from etl.transform.functions.duplicate_transform import remove_duplicates
from etl.transform.functions.interrogation_mark_transform import replace_interrogation_marks
from etl.transform.functions.float_transform import convert_to_float

def transform_pipeline(df: pd.DataFrame) -> pd.DataFrame:
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

