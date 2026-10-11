import numpy as np
import pandas as pd
import torch
from PIL import Image, ImageOps
from transformers import CLIPModel, CLIPProcessor

MODEL_NAME = "openai/clip-vit-base-patch32"


def as_tensor(output):
    """Newer versions of transformers return an object, older ones a tensor."""
    if torch.is_tensor(output):
        return output
    return output.pooler_output


catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})

print("Loading CLIP (the first run downloads about 600 MB)...")
model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
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
np.save("data/embeddings.npy", vectors)
print("Saved embeddings with shape", vectors.shape)