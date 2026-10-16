"""Step 2: teach a small model which two clothes belong in the same outfit.

Run from the project folder:   python src/polyvore_train.py
Reads data/polyvore_embeddings.npz, writes data/compat_model.joblib and prints the test score.

Idea: a REAL pair is two items from the same outfit. A FAKE pair keeps the first item and
swaps the second for an item of the same kind (same slot) from a different outfit.
Keeping the slot the same matters: otherwise the model would only learn "tops and
bottoms often appear together", which tells us nothing about taste.
"""

import random

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

from polyvore_common import SLOTS

SEED = 42
data = np.load("data/polyvore_embeddings.npz")
outfits, slots, vectors = data["outfits"], data["slots"], data["vectors"]
slot_index = {s: i for i, s in enumerate(SLOTS)}


def pair_features(a, b, slot_a, slot_b):
    """Order does not matter: (a, b) and (b, a) give the same numbers."""
    pair_type = np.zeros(len(SLOTS) * len(SLOTS))
    low, high = sorted([slot_index[slot_a], slot_index[slot_b]])
    pair_type[low * len(SLOTS) + high] = 1
    return np.concatenate([a * b, np.abs(a - b), pair_type])


# ---- group item numbers by outfit, and by slot ----
rows_of_outfit = {}
rows_of_slot = {s: [] for s in SLOTS}
for row, (outfit, slot) in enumerate(zip(outfits, slots)):
    rows_of_outfit.setdefault(outfit, []).append(row)
    rows_of_slot[slot].append(row)

# ---- split OUTFITS (not pairs) into train and test, so the test outfits are never seen ----
rng = random.Random(SEED)
outfit_names = sorted(rows_of_outfit)
rng.shuffle(outfit_names)
cut = int(len(outfit_names) * 0.8)
train_outfits, test_outfits = set(outfit_names[:cut]), set(outfit_names[cut:])


def make_pairs(outfit_set):
    X, y, sims = [], [], []
    for outfit in sorted(outfit_set):
        rows = rows_of_outfit[outfit]
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                a, b = rows[i], rows[j]
                if slots[a] == slots[b]:
                    continue                      # two tops in one outfit: not interesting
                X.append(pair_features(vectors[a], vectors[b], slots[a], slots[b]))
                y.append(1)
                sims.append(float(vectors[a] @ vectors[b]))
                # fake partner: same slot as b, but from a different outfit of this split
                for _ in range(20):
                    c = rng.choice(rows_of_slot[slots[b]])
                    if outfits[c] != outfit and outfits[c] in outfit_set:
                        X.append(pair_features(vectors[a], vectors[c], slots[a], slots[c]))
                        y.append(0)
                        sims.append(float(vectors[a] @ vectors[c]))
                        break
    return np.array(X), np.array(y), np.array(sims)


X_train, y_train, _ = make_pairs(train_outfits)
X_test, y_test, sim_test = make_pairs(test_outfits)
print(f"{len(y_train)} training pairs, {len(y_test)} test pairs (half real, half fake)")

model = LogisticRegression(max_iter=2000, C=0.5)
model.fit(X_train, y_train)
probability = model.predict_proba(X_test)[:, 1]

print()
print("Test results on outfits the model has never seen:")
print(f"  random guessing             : accuracy 50.0%")
print(f"  'similar-looking = matches' : AUC {roc_auc_score(y_test, sim_test):.3f}   (only cosine similarity)")
print(f"  trained model               : accuracy {accuracy_score(y_test, probability > 0.5):.1%}"
      f"   AUC {roc_auc_score(y_test, probability):.3f}")

joblib.dump({"model": model, "slots": SLOTS}, "data/compat_model.joblib")
print("Saved data/compat_model.joblib")
