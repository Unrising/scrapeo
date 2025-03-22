import os
import pandas as pd
from ml.functions.evaluate import evaluate_model
from ml.functions.prepare_data import prepare_data
from ml.functions.train_model import train_model

def run_ml_pipeline():
    gold_dir = "data/3_gold"
    files = [f for f in os.listdir(gold_dir) if f.endswith(".csv")]

    if not files:
        print("Aucun fichier trouvé dans data/3_gold/")
        return

    print("\nFichiers disponibles pour ML :")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    index = int(input("Choisis un fichier gold (numéro) : ").strip()) - 1
    selected_file = files[index]

    df = pd.read_csv(os.path.join(gold_dir, selected_file))

    print("\nColonnes disponibles pour prédiction :")
    for i, col in enumerate(df.columns[2:], 1):  # ignore Ville et Pays 
         
        print(f"{i}. {col}")

    target_idx = int(input("Choisis la variable cible à prédire (numéro) : ")) - 1
    target_column = df.columns[2:][target_idx]

    model_type = input("Modèle ? [linear / rf] : ").strip()
    model_type = "linear" if model_type.lower() == "linear" else "random_forest"

    # Pipeline ML
    X_train, X_test, y_train, y_test = prepare_data(df, target_column)
    model = train_model(X_train, y_train, model_type=model_type)
    predictions = evaluate_model(model, X_test, y_test)

    # Affiche un aperçu
    results = pd.DataFrame({"Réel": y_test, "Prévu": predictions})
    print("\n Prédictions :")
    print(results.head())

