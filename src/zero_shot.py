import numpy as np
import pandas as pd
import torch
from transformers import CLIPModel, CLIPProcessor

MODEL_NAME = "openai/clip-vit-base-patch32"
OCCASIONS = ["daily", "formal", "party", "date", "sport"]

# One sentence per occasion, in the SAME ORDER as OCCASIONS.
# Written once, before looking at any results.
PROMPTS = [
    "a photo of a casual everyday piece of clothing",
    "a photo of a formal elegant piece of clothing",
    "a photo of a glamorous party piece of clothing",
    "a photo of a romantic piece of clothing for a date",
    "a photo of a piece of sportswear",
]


def as_tensor(output):
    if torch.is_tensor(output):
        return output
    return output.pooler_output


catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})
image_vectors = torch.tensor(np.load("data/embeddings.npy"))

model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
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

print(f"CLIP zero-shot hit rate: {hits.mean():.1%}")
print(f"Random guess:            {chance:.1%}")
print(f"Always 'daily':          {always_daily:.1%}")

print("\nHow often CLIP predicted each occasion:")
print(pd.Series([OCCASIONS[i] for i in predicted]).value_counts())

results = catalogue[["id", "name"]].copy()
results["predicted"] = [OCCASIONS[i] for i in predicted]
results["hit"] = hits
results.to_csv("data/zero_shot_predictions.csv", index=False)
print("\nSaved data/zero_shot_predictions.csv")