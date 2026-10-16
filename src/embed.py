import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageOps
from transformers import CLIPModel, CLIPProcessor

from settings import as_tensor, embeddings_file, pick_model

key, model_name = pick_model()

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})

print(f"Loading {model_name} (the first run downloads about 600 MB)...")
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)
model.eval()

vectors = []
for number, item_id in enumerate(catalogue["id"], start=1):
    image = Image.open(f"data/photos/{item_id}.jpeg")
    image = ImageOps.exif_transpose(image).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        features = as_tensor(model.get_image_features(**inputs))

    features = features / features.norm(dim=-1, keepdim=True)
    vectors.append(features[0].numpy())
    print(f"{number}/{len(catalogue)}  {item_id}")

vectors = np.stack(vectors)
np.save(embeddings_file(key), vectors)
print("Saved", embeddings_file(key), "with shape", vectors.shape)
