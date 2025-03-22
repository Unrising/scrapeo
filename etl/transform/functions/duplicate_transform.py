import pandas as pd

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Supprime les lignes strictement dupliquées du DataFrame

    Retour :
        DataFrame sans doublons
    """
    return df.drop_duplicates()
