# AI usage

I used Claude (Anthropic) as a coding and writing assistant during this case study.

**What Claude helped with**
- Designed the weather and layer rules (temperature bands, layers per weather, rain boots) and the 5-question flow.
- Wrote the first versions of the CLIP embedding, zero-shot and classifier scripts. I ran them on my own photos and labels.
- Wrote the outfit engine (`engine.py`), the Streamlit website (`app.py`, `themes.py`, `layout.py`) and the rating logger (`rating_summary.py`). The outfit engine is plain rules, not AI.
- Explained CLIP and FashionCLIP, evaluation and overfitting, and helped plan the documentation.

**What I did myself**
- Photographed the 84 garments and wrote the labels in `catalogue.csv`.
- Ran all scripts, rated outfits, and decided which results to report.

**AI models used inside the project (not AI assistants)**
- CLIP `openai/clip-vit-base-patch32` (Radford et al., 2021) and FashionCLIP `patrickjohncyh/fashion-clip` (Chia et al., 2022, MIT licence, recommended by my professor). Both are used frozen, only to turn photos and text into numbers. Only the small logistic-regression classifier on top is trained, on my own photos.
