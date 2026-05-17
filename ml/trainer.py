import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.preprocessing import LabelEncoder

CLF_PATH     = "data/modelo_clasificacion.pkl"
REG_PATH     = "data/modelo_regresion.pkl"
ENCODER_PATH = "data/label_encoder.pkl"
FEATURES     = ['origen_lat', 'origen_lon', 'bateria_pct', 'dist_euclidiana']

def entrenar_modelo(df):
    if df is None or df.empty:
        print("!sin datos para entrenar")
        return False

    X = df[FEATURES].values

    #clasificacion: que electrolinera es la mejor
    le    = LabelEncoder()
    y_clf = le.fit_transform(df['electrolinera_id'].values)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y_clf, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_tr, y_tr)
    acc = accuracy_score(y_te, clf.predict(X_te))
    print(f"  [clasificacion entrenada  | Accuracy: {acc:.2%}")

    #regresion: distancia hasta la electrolinera
    y_reg = df['distancia_ruta_m'].values
    X_tr_r, X_te_r, y_tr_r, y_te_r = train_test_split(X, y_reg, test_size=0.2, random_state=42)

    reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    reg.fit(X_tr_r, y_tr_r)
    mae = mean_absolute_error(y_te_r, reg.predict(X_te_r))
    print(f"regresión entrenada      | MAE: {mae:.2f} m")

    #guardar
    os.makedirs("data", exist_ok=True)
    joblib.dump(clf,  CLF_PATH)
    joblib.dump(reg,  REG_PATH)
    joblib.dump(le,   ENCODER_PATH)
    print(f"modelos guardados en data/")

    print("\n importancia de caracteristicas:")
    for feat, imp in zip(FEATURES, clf.feature_importances_):
        barra = "█" * int(imp * 40)
        print(f"    {feat:<22} {barra} {imp:.4f}")

    return True

def cargar_modelos():
    if not os.path.exists(CLF_PATH):
        return None, None, None
    return joblib.load(CLF_PATH), joblib.load(REG_PATH), joblib.load(ENCODER_PATH)