from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

def train_model(X_train, y_train, model_type="random_forest"):
    """
    Entraîne un modèle de ML (régression linéaire ou forêt aléatoire)
    """
    if model_type == "linear":
        model = LinearRegression()
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X_train, y_train)
    return model