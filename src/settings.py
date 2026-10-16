"""Shared settings: which CLIP model to use and where its embeddings are saved.

Every script takes the model as an optional word after the file name:
    python src/embed.py               -> normal CLIP (the default)
    python src/embed.py fashionclip   -> FashionCLIP
"""

import sys

MODELS = {
    "clip": "openai/clip-vit-base-patch32",
    "fashionclip": "patrickjohncyh/fashion-clip",
}
OCCASIONS = ["daily", "formal", "party", "date", "sport"]


def pick_model():
    """Returns (short name, full model name) from the command line."""
    key = sys.argv[1] if len(sys.argv) > 1 else "clip"
    if key not in MODELS:
        sys.exit(f"Unknown model '{key}'. Choose one of: {', '.join(MODELS)}")
    return key, MODELS[key]


def embeddings_file(key):
    return f"data/embeddings_{key}.npy"


def as_tensor(output):
    """Newer versions of transformers return an object, older ones a tensor."""
    import torch
    if torch.is_tensor(output):
        return output
    return output.pooler_output
