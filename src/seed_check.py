import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict

OCCASIONS = ["daily", "formal", "party", "date", "sport"]

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})
X = np.load("data/embeddings.npy")
true = catalogue[OCCASIONS].values

rates = []
for seed in range(10):
    folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
    columns = []
    for occasion in OCCASIONS:
        y = catalogue[occasion].values
        model = LogisticRegression(max_iter=1000, class_weight="balanced")
        proba = cross_val_predict(model, X, y, cv=folds, method="predict_proba")[:, 1]
        columns.append(proba)
    best = np.column_stack(columns).argmax(axis=1)
    rates.append((true[np.arange(len(true)), best] == 1).mean())

print("Hit rate for 10 different splits:")
print([f"{r:.1%}" for r in rates])
print(f"Mean {np.mean(rates):.1%}, std {np.std(rates):.1%}")