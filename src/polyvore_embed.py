"""Step 1: turn a sample of Polyvore clothing photos into CLIP embeddings.

Run from the project folder:   python src/polyvore_embed.py
Reads the .parquet files in data/polyvore/ and writes data/polyvore_embeddings.npz.
It uses the SAME CLIP model as src/embed.py, so the numbers are comparable to your closet.
"""

import glob
import io
import random

import numpy as np
import pyarrow.parquet as pq
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from polyvore_common import SLOT_OF_CATEGORY, outfit_of

MODEL_NAME = "openai/clip-vit-base-patch32"
FILES = sorted(glob.glob("data/polyvore/*.parquet"))
HOW_MANY_OUTFITS = 2500        # more = better model but slower (about 3 clothing items per outfit)
SEED = 42                      # fixed seed so the sample is the same every run


def as_tensor(output):
    if torch.is_tensor(output):
        return output
    return output.pooler_output


if not FILES:
    raise SystemExit("No .parquet files found in data/polyvore/")

# ---- pass 1: read only the cheap columns, decide which outfits to use ----
print("Pass 1: reading item ids and categories (fast)...")
slots_in_outfit = {}      # outfit id -> {slot: how many}
for path in FILES:
    table = pq.read_table(path, columns=["item_ID", "category"]).to_pandas()
    for item_id, category in zip(table["item_ID"], table["category"]):
        slot = SLOT_OF_CATEGORY.get(category)
        if slot:
            slots_in_outfit.setdefault(outfit_of(item_id), set()).add(slot)

# an outfit is useful if it has clothes from at least 2 different slots
usable = sorted(o for o, slots in slots_in_outfit.items() if len(slots) >= 2)
random.Random(SEED).shuffle(usable)
chosen = set(usable[:HOW_MANY_OUTFITS])
print(f"{len(usable)} usable outfits in total, using {len(chosen)}")

# ---- pass 2: load the chosen photos and embed them ----
print("Loading CLIP...")
model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
model.eval()

ids, outfits, slots, vectors = [], [], [], []
for path in FILES:
    parquet = pq.ParquetFile(path)
    for batch in parquet.iter_batches(batch_size=64, columns=["item_ID", "category", "image"]):
        rows = batch.to_pylist()
        keep = [r for r in rows
                if outfit_of(r["item_ID"]) in chosen and r["category"] in SLOT_OF_CATEGORY]
        if not keep:
            continue
        images = [Image.open(io.BytesIO(r["image"]["bytes"])).convert("RGB") for r in keep]
        inputs = processor(images=images, return_tensors="pt")
        with torch.no_grad():
            features = as_tensor(model.get_image_features(**inputs))
        features = features / features.norm(dim=-1, keepdim=True)
        for r, vector in zip(keep, features.numpy()):
            ids.append(r["item_ID"])
            outfits.append(outfit_of(r["item_ID"]))
            slots.append(SLOT_OF_CATEGORY[r["category"]])
            vectors.append(vector)
        print(f"{len(ids)} photos embedded")

np.savez("data/polyvore_embeddings.npz", ids=np.array(ids), outfits=np.array(outfits),
         slots=np.array(slots), vectors=np.stack(vectors))
print("Saved data/polyvore_embeddings.npz with", len(ids), "items")
