import pandas as pd

def replace_interrogation_marks(df: pd.DataFrame, replacement_value: float = 0.0) -> pd.DataFrame:
    """
    Remplace les valeurs contenant "?" par une valeur (par défaut : 0.0)

    Paramètres :
        df : DataFrame d'entrée
        replacement_value : valeur à utiliser à la place du "?"

    Retour :
        DataFrame modifié
    """
    df = df.copy()
    return df.replace("?", replacement_value)

