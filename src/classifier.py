import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import precision_score, recall_score

OCCASIONS = ["daily", "formal", "party", "date", "sport"]

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})
X = np.load("data/embeddings.npy")
print("Embeddings:", X.shape, " Items:", len(catalogue))

# 5 folds: train on ~67 garments, test on ~17 the model has never seen
folds = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

probabilities = {}
print("\nPer occasion (tested on unseen garments):")
for occasion in OCCASIONS:
    y = catalogue[occasion].values
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    proba = cross_val_predict(model, X, y, cv=folds, method="predict_proba")[:, 1]
    guess = (proba >= 0.5).astype(int)
    probabilities[occasion] = proba
    precision = precision_score(y, guess, zero_division=0)
    recall = recall_score(y, guess, zero_division=0)
    print(f"{occasion:<8} items: {y.sum():>2}  precision: {precision:.2f}  recall: {recall:.2f}")

# Same hit rate as zero_shot.py, so the two are comparable
scores = np.column_stack([probabilities[o] for o in OCCASIONS])
best = scores.argmax(axis=1)
true = catalogue[OCCASIONS].values
hits = true[np.arange(len(true)), best] == 1
print(f"\nTrained classifier hit rate: {hits.mean():.1%}")
print("CLIP zero-shot hit rate:     61.9%")
print("Always 'daily':              70.2%")