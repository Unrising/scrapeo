from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
def evaluate_model(model, X_test, y_test):
    """
    Affiche la performance du modèle
    """
    predictions = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)

    print(f"\n Évaluation du modèle :")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²    : {r2:.2f}")

    return predictions
