import numpy as np
import pandas as pd
import torch
from transformers import CLIPModel, CLIPProcessor

from settings import OCCASIONS, as_tensor, embeddings_file, pick_model

key, model_name = pick_model()

# One sentence per occasion, in the SAME ORDER as OCCASIONS.
# Written once, before looking at any results. The same sentences are used for
# every model, so the comparison is fair. Do not tune them on your own photos.
PROMPTS = [
    "a photo of a casual everyday piece of clothing",
    "a photo of a formal elegant piece of clothing",
    "a photo of a glamorous party piece of clothing",
    "a photo of a romantic piece of clothing for a date",
    "a photo of a piece of sportswear",
]

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})
image_vectors = torch.tensor(np.load(embeddings_file(key)))

model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()

inputs = processor(text=PROMPTS, return_tensors="pt", padding=True)
with torch.no_grad():
    text_vectors = as_tensor(model.get_text_features(**inputs))
text_vectors = text_vectors / text_vectors.norm(dim=-1, keepdim=True)

# similarity of every photo with every sentence: shape (items, 5)
similarity = image_vectors @ text_vectors.T
predicted = similarity.argmax(dim=1).numpy()

truth = catalogue[OCCASIONS].values              # 0/1 labels, shape (items, 5)
hits = truth[np.arange(len(truth)), predicted]   # 1 if the guess is one of the true occasions

chance = truth.sum(axis=1).mean() / len(OCCASIONS)   # expected hit rate of a random guess
always_daily = truth[:, 0].mean()                     # hit rate of always answering "daily"

print(f"Model: {model_name}")
print(f"Zero-shot hit rate: {hits.mean():.1%}")
print(f"Random guess:       {chance:.1%}")
print(f"Always 'daily':     {always_daily:.1%}")

print("\nHow often the model predicted each occasion:")
print(pd.Series([OCCASIONS[i] for i in predicted]).value_counts())

results = catalogue[["id", "name"]].copy()
results["predicted"] = [OCCASIONS[i] for i in predicted]
results["hit"] = hits
results.to_csv(f"data/zero_shot_predictions_{key}.csv", index=False)
print(f"\nSaved data/zero_shot_predictions_{key}.csv")
