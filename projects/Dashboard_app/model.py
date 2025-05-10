# model.py
import io, base64, warnings, matplotlib
import mlflow
import numpy as np
import pandas as pd
matplotlib.use("Agg") 
import matplotlib.pyplot as plt


from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, RocCurveDisplay, accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

ALGO_MAP = {
    "logreg":  lambda hp: LogisticRegression(
                    C=float(hp["C"]), penalty=hp["penalty"],
                    solver="liblinear", max_iter=500),
    "svm":     lambda hp: SVC(
                    C=float(hp["C"]), gamma=float(hp["gamma"]),
                    probability=True),
    "knn":     lambda hp: KNeighborsClassifier(
                    n_neighbors=int(hp["k"]), metric="minkowski"),
    "gb":      lambda hp: GradientBoostingClassifier(
                    n_estimators=int(hp["n_estimators"]),
                    learning_rate=float(hp["lr"]),
                    max_depth=int(hp["max_depth"]))
}


raw = load_breast_cancer(as_frame=True)
X = raw["data"]
y = raw["target"]
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

def train_eval(algo_key, hp):
    """Train chosen algo, return metrics & ROC PNG (b64)."""
    model = ALGO_MAP[algo_key](hp)

    pipe = Pipeline([
        ("scaler", StandardScaler()),  # harmless for tree‑based too
        ("clf", model)
    ]).fit(X_tr, y_tr)

    y_prob = pipe.predict_proba(X_te)[:, 1]
    auc  = roc_auc_score(y_te, y_prob)
    acc  = accuracy_score(y_te, pipe.predict(X_te))

    # ROC plot
    fig, ax = plt.subplots(figsize=(4,4))
    RocCurveDisplay.from_predictions(y_te, y_prob, ax=ax)
    ax.set_title(f"{algo_key.upper()}  AUC={auc:.3f}")
    buf = io.BytesIO(); fig.tight_layout(); fig.savefig(buf, format="png"); plt.close(fig)
    roc_b64 = base64.b64encode(buf.getvalue()).decode("utf8")

    # ── MLflow logging ────────────────────────────────────
    with mlflow.start_run(run_name=algo_key):
        mlflow.log_params({"algo": algo_key, **hp})
        mlflow.log_metrics({"AUC": auc, "Accuracy": acc})
        mlflow.log_figure(fig, "roc.png")  # automatically closes figure

    return {"auc": auc, "accuracy": acc, "roc_plot": roc_b64}
