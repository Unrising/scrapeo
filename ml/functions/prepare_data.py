import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_data(df: pd.DataFrame, target_column: str):
    """
    Prépare les données pour l'entraînement : séparation X / y + split train/test
    """
    df = df.dropna(subset=[target_column])
    X = df.drop(columns=["Ville", "Pays", target_column])
    y = df[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=42)
