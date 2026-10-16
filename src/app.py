import csv
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from engine import build_outfits, rank_outfits
from layout import collage_svg, nav_html
from themes import THEMES, WELCOME, apply_theme, landing_css

st.set_page_config(page_title="Pearlfect", page_icon="🪞", layout="wide")

PHOTO_FOLDER = Path("data/Photos")
RATINGS_FILE = Path("data/ratings.csv")
OCCASIONS = ["daily", "formal", "party", "date", "sport"]
COLOURS = ["no preference", "black", "white", "grey", "beige", "navy", "denim",
           "brown", "maroon", "red", "pink", "yellow", "orange", "green",
           "blue", "purple"]
SLOT_TITLES = {
    "base": "Tops",
    "mid": "Mid layers",
    "outer": "Jackets and coats",
    "bottom": "Bottoms",
    "accessory": "Accessories",
}
LAYER_CHOICES = {"Let the weather decide": None, "Just a top": 1, "Top + mid layer": 2}

# Streamlit re-runs this whole file after every click, so anything that has to
# survive a click (which page we are on, which vibe was picked) lives here.
if "page" not in st.session_state:
    st.session_state.page = "vibe"
if "theme" not in st.session_state:
    st.session_state.theme = "gingham"


def go(page):
    st.session_state.page = page


def save_rating(score, outfit, context):
    """Add one line to data/ratings.csv. This only logs; it does not change the engine."""
    is_new = not RATINGS_FILE.exists()
    with open(RATINGS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if is_new:
            writer.writerow(["time", "temp_c", "raining", "occasion", "style", "layers",
                             "colour", "round", "outfit", "score"])
        writer.writerow([datetime.now().isoformat(timespec="seconds"), context["temp_c"],
                         context["raining"], context["occasion"], context["style"],
                         context["layers"], context["colour"], context["round"],
                         " | ".join(outfit), score])
    st.session_state.saved_msg = f"Saved: {score} out of 5"


def next_round():
    st.session_state.round = st.session_state.get("round", 0) + 1


def choose_theme(key):
    st.session_state.theme = key
    st.session_state.page = "closet"


@st.cache_data
def load_catalogue():
    return pd.read_csv("data/catalogue.csv", dtype={"id": str})


def photo_of(item_id):
    """Path of an item's photo, or None if the file is missing."""
    for extension in (".jpeg", ".jpg"):
        path = PHOTO_FOLDER / f"{item_id}{extension}"
        if path.exists():
            return str(path)
    return None


# ---------------------------------------------------------------- page 1
def vibe_page():
    with st.container(key="landing-top"):
        st.markdown(nav_html(1), unsafe_allow_html=True)
        st.markdown('<p class="eyebrow">Your closet, mixed for today</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="mega">Pearlfect<span class="dot">.</span></h1>', unsafe_allow_html=True)
        st.markdown('<p class="lede">Tell it the weather and the plan. It builds the outfit '
                    'from clothes you already own. Start by picking a vibe: it only changes '
                    'the colours.</p>', unsafe_allow_html=True)

    with st.container(key="vibes"):
        st.markdown('<h2 class="section-title">Pick your vibe</h2>', unsafe_allow_html=True)
        keys = list(THEMES)
        for start in range(0, len(keys), 4):
            columns = st.columns(4, gap="medium")
            for column, key in zip(columns, keys[start:start + 4]):
                theme = THEMES[key]
                with column:
                    with st.container(key=f"vibe-{key}"):
                        mini = collage_svg(theme["collage"], width=500, height=190,
                                           seed=len(key), small=True)
                        st.markdown(f'<div class="mini">{mini}</div>', unsafe_allow_html=True)
                        st.markdown(
                            f'<div class="vibe-text"><b>{theme["label"]}</b>'
                            f'<small>{theme["tagline"]}</small></div>',
                            unsafe_allow_html=True)
                        st.button("Choose", key=f"choose_{key}", on_click=choose_theme, args=(key,))


# ---------------------------------------------------------------- page 2
def closet_page():
    catalogue = load_catalogue()
    theme = THEMES[st.session_state.theme]
    st.markdown(nav_html(2), unsafe_allow_html=True)
    with st.container(key="hero-small"):
        st.markdown(collage_svg(theme["collage"], width=600, height=420, small=True), unsafe_allow_html=True)
        st.markdown(f'<p class="eyebrow">{len(catalogue)} pieces</p>', unsafe_allow_html=True)
        st.markdown('<h1 class="mega">Your closet</h1>', unsafe_allow_html=True)
        left, right, _ = st.columns([1.4, 1.4, 4])
        left.button("Change vibe", on_click=go, args=("vibe",))
        right.button("Get my outfit", on_click=go, args=("questions",))
    st.markdown(f'<div class="ribbon"></div>', unsafe_allow_html=True)

    with st.container(key="closet-grid"):
        slots = [slot for slot in SLOT_TITLES if slot in catalogue["slot"].values]
        tabs = st.tabs([SLOT_TITLES[slot] for slot in slots])
        for tab, slot in zip(tabs, slots):
            with tab:
                items = catalogue[catalogue["slot"] == slot]
                for start in range(0, len(items), 5):
                    row = items.iloc[start:start + 5]
                    columns = st.columns(5)
                    for column, (_, item) in zip(columns, row.iterrows()):
                        path = photo_of(item["id"])
                        if path:
                            column.image(path, caption=item["name"])


# ---------------------------------------------------------------- page 3
def questions_page():
    catalogue = load_catalogue()
    st.markdown(nav_html(3), unsafe_allow_html=True)
    with st.container(key="questions-wrap"):
        st.markdown('<h1 class="mega" style="margin-top:1.5rem">What are we wearing?</h1>',
                    unsafe_allow_html=True)
        ask_col, look_col = st.columns([1, 2], gap="large")

        with ask_col:
            with st.container(key="ask"):
                st.markdown('<span class="tab">Today\'s questions</span>', unsafe_allow_html=True)
                temp_c = st.slider("Temperature today (°C)", -5, 40, 18)
                is_raining = st.checkbox("It's raining")
                occasion = st.selectbox("Occasion", OCCASIONS)
                style = st.slider("Style: 1 = comfy, 3 = formal", 1, 3, 2)
                layer_choice = st.radio("Layers under my coat", list(LAYER_CHOICES), horizontal=True)
                colour = st.selectbox("Preferred colour", COLOURS)
            st.button("Back to my closet", on_click=go, args=("closet",))

        with look_col:
            photo_lookup = dict(zip(catalogue["name"], catalogue["id"]))
            notes = []
            outfits, missing_slot = build_outfits(
                catalogue, temp_c, occasion, is_raining,
                upper_layers=LAYER_CHOICES[layer_choice], notes=notes)

            if is_raining:
                st.info("It's raining: wear your raincoat over any outfit.")
            for note in dict.fromkeys(notes):
                st.info(note)
            if missing_slot:
                st.warning(f"No items found for: {missing_slot}")
                return

            preferred = None if colour == "no preference" else colour
            if "round" not in st.session_state:
                st.session_state.round = 0
            best = rank_outfits(outfits, catalogue, style, preferred, top=3,
                                temp_c=temp_c, skip=st.session_state.round)
            if not best:
                st.session_state.round = 0
                best = rank_outfits(outfits, catalogue, style, preferred, top=3, temp_c=temp_c)
            for number, (score, outfit) in enumerate(best, start=1):
                with st.container(key=f"look-{number}"):
                    st.markdown(f'<span class="tab">Look 0{number}</span>', unsafe_allow_html=True)
                    columns = st.columns(len(outfit))
                    for column, name in zip(columns, outfit):
                        path = photo_of(photo_lookup[name])
                        if path:
                            column.image(path, caption=name)
                    st.caption("Rate this look (1 = no way, 5 = perfect)")
                    context = {"temp_c": temp_c, "raining": is_raining, "occasion": occasion,
                               "style": style, "layers": layer_choice, "colour": colour,
                               "round": st.session_state.round}
                    stars = st.columns([1, 1, 1, 1, 1, 6])
                    for score, star in enumerate(stars[:5], start=1):
                        star.button(str(score), key=f"rate-{number}-{score}",
                                    on_click=save_rating, args=(score, outfit, context))
            if "saved_msg" in st.session_state:
                st.success(st.session_state.pop("saved_msg"))
            st.button("Show me different looks", on_click=next_round)


# ---------------------------------------------------------------- main
page = st.session_state.page
if page == "vibe":
    apply_theme(WELCOME, previews=THEMES)
    st.markdown(landing_css(), unsafe_allow_html=True)
    vibe_page()
else:
    apply_theme(THEMES[st.session_state.theme])
    if page == "closet":
        closet_page()
    else:
        questions_page()
