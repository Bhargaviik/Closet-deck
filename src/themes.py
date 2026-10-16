"""Vibes (colour + type + shape themes) for Pearlfect.

Every vibe is a dictionary. apply_theme() turns one into CSS for Streamlit.
Nothing here knows anything about the person using the app: a vibe is a look
they pick, not a category they belong to.

To add a vibe: copy one dictionary in THEMES, change the values, give it a new key.

Two layouts exist:
  "editorial" - big airy serif headlines, soft pill buttons (the TERRA look)
  "chunky"    - huge bold uppercase headlines, thick outlines (the Hot Core look)
"""

import colorsys
from urllib.parse import quote

import streamlit as st

from layout import spiral_svg, torn_clip

# The landing page, before anyone has picked a vibe.
RED = "#800e13"
CREAM = "#fff7ea"
PINK_LINES = "rgba(240, 150, 175, 0.55)"     # the grid lines on the wallpaper
SPIRAL_LIGHT = "#f6b4c4"
SPIRAL_DARK = "#ec86a1"
BUTTER = "#EBDD91"

WELCOME = {
    "layout": "editorial",
    "paper": CREAM,
    "paper_image": "none",
    "text": RED,
    "heading": RED,
    "accent": RED,
    "accent_text": CREAM,
    "panel": RED,
    "panel_text": CREAM,
    "slider_hue": 30,
    "card_bg": CREAM,
    "card_text": RED,
    "card_border": RED,
    "input_bg": CREAM,
    "input_text": RED,
    "pattern": "none",
    "pattern_size": "auto",
    "heading_font": "Fraunces",
    "body_font": "Jost",
    "fonts": "family=Fraunces:wght@400;600&family=Jost:wght@400;500;700",
    "photo_style": "torn",
}

THEMES = {
    "gingham": {
        "label": "Gingham Pink",
        "tagline": "Red gingham, pink, picnic energy",
        "swatches": ["#d62839", "#f4a6bb", "#fff4f6"],
        "layout": "chunky",
        "paper": "#fff0f3",
        "paper_image": "none",
        "text": "#4a1420",
        "heading": "#c1121f",
        "accent": "#d62839",
        "accent_text": "#ffffff",
        "panel": "#d62839",
        "panel_text": "#ffffff",
        "slider_hue": 48,
        "slider_filter": "grayscale(1) brightness(6)",
        "card_bg": "#ffffff",
        "card_text": "#4a1420",
        "card_border": "#c1121f",
        "input_bg": "#fff6f8",
        "input_text": "#4a1420",
        "pattern": (
            "linear-gradient(rgba(214, 40, 57, 0.34) 50%, transparent 50%), "
            "linear-gradient(90deg, rgba(214, 40, 57, 0.34) 50%, transparent 50%), #f9bfcd"
        ),
        "pattern_size": "56px 56px",
        "collage": ["#e63950", "#f4a6bb", "#fff6f8", "#c1121f"],
        "heading_font": "Alfa Slab One",
        "body_font": "DM Sans",
        "fonts": "family=Alfa+Slab+One&family=DM+Sans:wght@400;500;700",
        "photo_style": "round",
    },
    "aurora": {
        "label": "Northern Lights",
        "tagline": "Deep purple sky, glowing green",
        "swatches": ["#130726", "#7a5cff", "#58f5b0"],
        "layout": "editorial",
        "paper": "#130726",
        "paper_image": (
            "radial-gradient(ellipse 70% 40% at 12% 0%, rgba(70, 255, 175, 0.40), transparent 60%), "
            "radial-gradient(ellipse 60% 45% at 90% 6%, rgba(150, 95, 255, 0.50), transparent 60%)"
        ),
        "text": "#ece6ff",
        "heading": "#7dffc4",
        "accent": "#58f5b0",
        "accent_text": "#1a0933",
        "panel": "#2b1559",
        "panel_text": "#ece6ff",
        "slider_hue": 155,
        "card_bg": "#1f0f42",
        "card_text": "#ece6ff",
        "card_border": "#58f5b0",
        "input_bg": "#130726",
        "input_text": "#ece6ff",
        "pattern": (
            "linear-gradient(90deg, #58f5b0, #7a5cff, #58f5b0)"
        ),
        "pattern_size": "auto",
        "collage": ["#58f5b0", "#2b1559", "#7a5cff", "#1d9a72"],
        "heading_font": "Space Grotesk",
        "body_font": "Inter",
        "fonts": "family=Space+Grotesk:wght@400;500;700&family=Inter:wght@400;500;700",
        "photo_style": "round",
    },
    "meadow": {
        "label": "Sunny Meadow",
        "tagline": "Fresh green, bright yellow, stripes",
        "swatches": ["#1f6f43", "#ffd93b", "#fff9d6"],
        "layout": "chunky",
        "paper": "#fffbe0",
        "paper_image": "none",
        "text": "#16402a",
        "heading": "#1f6f43",
        "accent": "#1f6f43",
        "accent_text": "#ffe55c",
        "panel": "#1f6f43",
        "panel_text": "#fffbe0",
        "slider_hue": 52,
        "card_bg": "#fff3b0",
        "card_text": "#16402a",
        "card_border": "#1f6f43",
        "input_bg": "#ffffff",
        "input_text": "#16402a",
        "pattern": "repeating-linear-gradient(90deg, #1f6f43 0px, #1f6f43 34px, #ffd93b 34px, #ffd93b 68px)",
        "pattern_size": "auto",
        "collage": ["#ffd93b", "#1f6f43", "#fff3b0", "#3fa86b"],
        "heading_font": "Bricolage Grotesque",
        "body_font": "DM Sans",
        "fonts": "family=Bricolage+Grotesque:wght@500;800&family=DM+Sans:wght@400;500;700",
        "photo_style": "round",
    },
    "orchid": {
        "label": "Orchid Wine",
        "tagline": "Wine red, algae green, soft wasabi",
        "swatches": ["#afa231", "#4c0004", "#dcd189"],
        "layout": "chunky",
        "paper": "#dcd189",
        "paper_image": "none",
        "text": "#4c0004",
        "heading": "#4c0004",
        "accent": "#4c0004",
        "accent_text": "#dcd189",
        "panel": "#4c0004",
        "panel_text": "#dcd189",
        "slider_hue": 62,
        "card_bg": "#f3eeb9",
        "card_text": "#4c0004",
        "card_border": "#4c0004",
        "input_bg": "#fbf8dc",
        "input_text": "#4c0004",
        "pattern": "repeating-linear-gradient(135deg, #afa231 0px, #afa231 3px, #dcd189 3px, #dcd189 22px)",
        "pattern_size": "auto",
        "collage": ["#4c0004", "#afa231", "#f3eeb9", "#4c0004"],
        "heading_font": "Josefin Sans",
        "body_font": "Josefin Sans",
        "fonts": "family=Josefin+Sans:wght@400;600;700",
        "photo_style": "square",
    },
    "spaghetti": {
        "label": "Sunday Pasta",
        "tagline": "Rust, butter yellow, blue, picnic cloth",
        "swatches": ["#ba3801", "#ffec89", "#4a69b3"],
        "layout": "chunky",
        "paper": "#fffdf0",
        "paper_image": "none",
        "text": "#1d2b57",
        "heading": "#ba3801",
        "accent": "#4a69b3",
        "accent_text": "#ffffff",
        "panel": "#4a69b3",
        "panel_text": "#ffffff",
        "slider_hue": 50,
        "card_bg": "#ffec89",
        "card_text": "#1d2b57",
        "card_border": "#4a69b3",
        "input_bg": "#ffffff",
        "input_text": "#1d2b57",
        "pattern": (
            "linear-gradient(rgba(255, 214, 64, 0.60) 50%, transparent 50%), "
            "linear-gradient(90deg, rgba(255, 214, 64, 0.60) 50%, transparent 50%), #fffdf0"
        ),
        "pattern_size": "64px 64px",
        "collage": ["#ba3801", "#4a69b3", "#ffec89", "#ba3801"],
        "heading_font": "Poppins",
        "body_font": "Poppins",
        "fonts": "family=Poppins:wght@400;500;600;800",
        "photo_style": "round",
    },
    "pear": {
        "label": "Pear Orchard",
        "tagline": "Pear gold, tomato, mint and cream",
        "swatches": ["#eebf43", "#b94624", "#f2e7cb", "#94b38a"],
        "layout": "editorial",
        "paper": "#f2e7cb",
        "paper_image": "none",
        "text": "#4a2a1a",
        "heading": "#b94624",
        "accent": "#b94624",
        "accent_text": "#fff4de",
        "panel": "#94b38a",
        "panel_text": "#26331f",
        "slider_hue": 14,
        "card_bg": "#fbf4e1",
        "card_text": "#4a2a1a",
        "card_border": "#b94624",
        "input_bg": "#ffffff",
        "input_text": "#26331f",
        "pattern": (
            "radial-gradient(circle, #94b38a 0px, #94b38a 9px, transparent 10px) 0 0, "
            "radial-gradient(circle, #eebf43 0px, #eebf43 9px, transparent 10px) 36px 36px, #f2e7cb"
        ),
        "pattern_size": "72px 72px",
        "collage": ["#b94624", "#94b38a", "#fbf4e1", "#eebf43"],
        "heading_font": "Fraunces",
        "body_font": "DM Sans",
        "fonts": "family=Fraunces:wght@400;600&family=DM+Sans:wght@400;500;700",
        "photo_style": "torn",
    },
    "lotus": {
        "label": "Lotus Pond",
        "tagline": "Deep greens, brandy, pale copper",
        "swatches": ["#202808", "#6a784d", "#dec59e", "#c4866d"],
        "layout": "editorial",
        "paper": "#202808",
        "paper_image": (
            "radial-gradient(circle at 10% 15%, rgba(106, 120, 77, 0.45) 0%, transparent 34%), "
            "radial-gradient(circle at 90% 8%, rgba(196, 134, 109, 0.25) 0%, transparent 30%)"
        ),
        "text": "#dec59e",
        "heading": "#c4866d",
        "accent": "#c4866d",
        "accent_text": "#202808",
        "panel": "#33432b",
        "panel_text": "#dec59e",
        "slider_hue": 17,
        "card_bg": "#33432b",
        "card_text": "#dec59e",
        "card_border": "#6a784d",
        "input_bg": "#202808",
        "input_text": "#dec59e",
        "pattern": "repeating-linear-gradient(90deg, #6a784d 0px, #6a784d 2px, #33432b 2px, #33432b 18px)",
        "pattern_size": "auto",
        "collage": ["#c4866d", "#33432b", "#6a784d", "#dec59e"],
        "heading_font": "Syne",
        "body_font": "DM Sans",
        "fonts": "family=Syne:wght@500;700;800&family=DM+Sans:wght@400;500;700",
        "photo_style": "arch",
    },
    "leaf": {
        "label": "Autumn Leaf",
        "tagline": "Space cadet, slate, tan, coffee, plum",
        "swatches": ["#25344f", "#617891", "#d5b893", "#6f4d38", "#632024"],
        "layout": "editorial",
        "paper": "#25344f",
        "paper_image": (
            "linear-gradient(165deg, rgba(37, 52, 79, 0) 45%, rgba(99, 32, 36, 0.85) 100%)"
        ),
        "text": "#e6d3b8",
        "heading": "#d5b893",
        "accent": "#d5b893",
        "accent_text": "#25344f",
        "panel": "#632024",
        "panel_text": "#e6d3b8",
        "slider_hue": 33,
        "card_bg": "#d5b893",
        "card_text": "#3b2619",
        "card_border": "#6f4d38",
        "input_bg": "#f1e4cf",
        "input_text": "#3b2619",
        "pattern": "repeating-linear-gradient(60deg, #617891 0px, #617891 2px, #25344f 2px, #25344f 30px)",
        "pattern_size": "auto",
        "collage": ["#d5b893", "#617891", "#6f4d38", "#632024"],
        "heading_font": "Cormorant Garamond",
        "body_font": "DM Sans",
        "fonts": "family=Cormorant+Garamond:wght@500;700&family=DM+Sans:wght@400;500;700",
        "photo_style": "torn",
    },
}


def photo_css(style, border, shadow):
    """How the clothing photos are framed."""
    if style == "torn":
        return f"clip-path: {torn_clip()}; border: none;"
    if style == "arch":
        return f"border-radius: 999px 999px 14px 14px; border: 2px solid {border};"
    if style == "square":
        return f"border-radius: 3px; border: 3px solid {border}; box-shadow: 5px 5px 0 {shadow};"
    return f"border-radius: 16px; border: 2px solid {border};"


def preview_css(themes):
    """One block of CSS per vibe card on the landing page, in that vibe's own colours."""
    rules = ""
    for key, t in themes.items():
        rules += f"""
.st-key-vibe-{key} {{
    background: {t["paper"]};
    background-image: {t["paper_image"]};
    border: 3px solid {t["card_border"]};
    border-radius: 22px;
    overflow: hidden;
    gap: 0 !important;
}}
.st-key-vibe-{key} .vibe-text b {{ font-family: '{t["heading_font"]}', serif; color: {t["heading"]}; }}
.st-key-vibe-{key} .vibe-text small {{ color: {t["text"]}; }}
.st-key-vibe-{key} .stButton > button {{ background: {t["accent"]}; border-color: {t["accent"]}; }}
.st-key-vibe-{key} .stButton > button p {{ color: {t["accent_text"]}; }}
"""
    return rules


def hue_of(hex_colour):
    """Hue of a colour in degrees (0-360)."""
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return round(colorsys.rgb_to_hsv(r, g, b)[0] * 360)


def build_css(t, previews=None):
    """Turn one vibe into one block of CSS."""
    chunky = t["layout"] == "chunky"
    turn = hue_of(t["accent"])
    slide = t["slider_hue"]

    if chunky:
        mega = ("font-size: clamp(3.2rem, 8.6vw, 8.2rem); line-height: 0.9; text-transform: uppercase; "
                "letter-spacing: -0.005em; font-weight: 800;")
        button = (f"border: 3px solid {t['card_border']}; box-shadow: 4px 4px 0 {t['card_border']}; "
                  "padding: 0.6rem 1.7rem;")
        panel_radius = "6px"
        card_radius = "6px"
    else:
        mega = ("font-size: clamp(3.4rem, 7.4vw, 7.2rem); line-height: 0.95; letter-spacing: -0.02em; "
                "font-weight: 500;")
        button = "border: none; box-shadow: none; padding: 0.7rem 1.9rem;"
        panel_radius = "26px"
        card_radius = "22px"
    heading_font = t["heading_font"]

    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?{t["fonts"]}&display=swap');

/* ---------- page: paper colour, a little grain, no Streamlit chrome ---------- */
.stApp {{
    background-color: {t["paper"]};
    background-image: {t["paper_image"]};
    background-attachment: fixed;
    color: {t["text"]};
    font-family: '{t["body_font"]}', sans-serif;
}}
.stApp::after {{
    content: ""; position: fixed; inset: 0; pointer-events: none; z-index: 999;
    opacity: 0.16;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}}
[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer {{ display: none !important; }}
[data-testid="stMainBlockContainer"] {{ max-width: 100% !important; padding: 0 0 4rem 0 !important; }}
[data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {{ gap: 0; }}

/* ---------- text ---------- */
.stApp p, .stApp li, .stApp label, .stApp small, [data-testid="stMarkdownContainer"],
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {{
    color: {t["text"]}; font-family: '{t["body_font"]}', sans-serif;
}}
.stApp h1, .stApp h2, .stApp h3, .mega, .section-title {{
    font-family: '{heading_font}', serif; color: {t["heading"]};
}}
.nav {{
    display: flex; justify-content: space-between; align-items: center;
    padding: 1.3rem 6vw; position: relative; z-index: 5;
    font-size: 0.78rem; letter-spacing: 0.32em; text-transform: uppercase; color: {t["heading"]};
}}
.nav .logo {{ font-weight: 700; font-family: '{heading_font}', serif; letter-spacing: 0.28em; }}
.stApp p.eyebrow {{ font-size: 0.78rem !important; letter-spacing: 0.3em; text-transform: uppercase; margin: 0 0 1.1rem 0; color: {t["text"]}; }}
.stApp h1.mega, .stApp .mega {{ {mega.replace(";"," !important;")} margin: 0 0 1.2rem 0 !important; padding: 0 !important; }}
.stApp h2.section-title {{ font-size: clamp(2.2rem, 4.6vw, 4.2rem) !important; line-height: 0.95; margin: 0 0 1.2rem 0; padding: 0; {"text-transform: uppercase; font-weight: 800;" if chunky else "font-weight: 500;"} }}
.lede {{ font-size: 1.15rem; line-height: 1.5; max-width: 30rem; margin: 0 0 1.4rem 0; color: {t["text"]}; }}

/* ---------- hero: the torn paper collage sits behind the words ---------- */
[class*="st-key-hero"] {{ position: relative; overflow: hidden; padding: 4rem 6vw 7rem 6vw; min-height: 600px; }}
[class*="st-key-hero"] > [data-testid="stElementContainer"]:first-child {{
    position: absolute; inset: 0; z-index: 0; height: 100%;
}}
[class*="st-key-hero"] > [data-testid="stElementContainer"]:first-child div {{ height: 100%; }}
[class*="st-key-hero"] > [data-testid="stElementContainer"]:not(:first-child) {{ position: relative; z-index: 2; max-width: 40rem; }}
.st-key-hero-small {{ min-height: 340px !important; padding-bottom: 3rem !important; }}
.st-key-hero-small > [data-testid="stElementContainer"]:first-child {{ left: auto; right: 0; width: 52% !important; }}
.st-key-hero-small > [data-testid="stElementContainer"]:first-child * {{ width: 100% !important; max-width: 100% !important; }}
.st-key-hero-small svg.collage {{ height: 100% !important; }}
.st-key-hero-small [data-testid="stHorizontalBlock"] {{ gap: 0.8rem; }}
svg.collage {{ width: 100%; height: 100%; display: block; }}
.ribbon {{ height: 54px; background: {t["pattern"]}; background-size: {t["pattern_size"]}; border-top: 3px solid {t["card_border"]}; border-bottom: 3px solid {t["card_border"]}; }}

/* ---------- buttons ---------- */
.stButton > button {{
    background: {t["accent"]}; border-radius: 999px; {button}
    transition: transform 0.12s ease, box-shadow 0.12s ease;
}}
.stButton > button p {{ color: {t["accent_text"]}; font-weight: 700; letter-spacing: 0.06em; }}
.stButton > button:hover {{ background: {t["accent"]}; transform: translateY(-2px); border-color: {t["card_border"] if chunky else "transparent"}; }}
.stButton > button:active {{ transform: translateY(1px); }}

/* ---------- landing page vibe cards ---------- */
.st-key-vibes {{ padding: 1rem 6vw 5rem 6vw; }}
.vibe-text {{ padding: 0.9rem 1rem 1rem 1rem; text-align: left; }}
.vibe-text b {{ font-size: 1.15rem; display: block; margin-bottom: 0.2rem; }}
.vibe-text small {{ font-size: 0.82rem; line-height: 1.3; display: block; }}
.mini {{ height: 150px; overflow: hidden; }}
.mini svg {{ width: 100%; height: 100%; display: block; }}
[class*="st-key-vibe-"] [data-testid="stElementContainer"]:has(.stButton) {{ padding: 0.4rem 1rem 1rem 1rem; }}

/* ---------- questions panel and outfit cards ---------- */
.st-key-ask {{
    background: {t["panel"]}; border-radius: {panel_radius}; padding: 2.4rem 1.8rem 1.8rem 1.8rem; position: relative;
    margin-top: 2.6rem; border: 3px solid {t["card_border"]};
}}
.st-key-ask p, .st-key-ask label, .st-key-ask span, .st-key-ask [data-testid="stWidgetLabel"] p {{ color: {t["panel_text"]}; }}
.tab {{
    position: absolute; top: -2.05rem; left: 1.4rem; padding: 0.45rem 1.1rem 0.35rem 1.1rem;
    background: {t["card_border"]}; color: {t["paper"]}; border-radius: 10px 10px 0 0;
    font-size: 0.72rem; letter-spacing: 0.22em; text-transform: uppercase; font-weight: 700;
}}
[class*="st-key-look-"] {{
    background: {t["card_bg"]}; border: 3px solid {t["card_border"]}; border-radius: {card_radius};
    padding: 1.6rem 1.4rem 1.2rem 1.4rem; margin: 2.6rem 0 0 0; position: relative;
}}
[class*="st-key-look-"] p, [class*="st-key-look-"] [data-testid="stCaptionContainer"] p {{ color: {t["card_text"]}; }}
[class*="st-key-look-"] .tab {{ left: 1.2rem; }}

/* dropdowns, sliders, radios, checkboxes */
[data-testid="stSelectbox"] [role="group"] {{
    background: {t["input_bg"]} !important; border: 2px solid {t["card_border"]} !important; border-radius: 12px !important;
}}
[data-testid="stSelectbox"] input {{ color: {t["input_text"]} !important; -webkit-text-fill-color: {t["input_text"]} !important; }}
[data-testid="stSelectbox"] svg {{ color: {t["input_text"]}; }}
[data-testid="stSelectboxVirtualDropdown"] {{ background: {t["input_bg"]}; border: 2px solid {t["card_border"]}; border-radius: 12px; }}
[data-testid="stSelectboxVirtualDropdown"] * {{ color: {t["input_text"]} !important; }}
[data-testid="stSlider"] [role="group"] > [data-orientation="horizontal"] {{ filter: {t.get("slider_filter", f"hue-rotate({slide}deg)")}; }}
[data-testid="stSlider"] [role="group"] > [data-orientation="horizontal"] p {{ filter: {"none" if "slider_filter" in t else f"hue-rotate({-slide}deg)"}; }}
[data-testid="stCheckbox"] label > div:first-of-type, [data-testid="stRadio"] label > div:first-of-type {{ filter: hue-rotate({slide}deg); }}
[data-testid="stTabs"] [role="tablist"] {{ filter: hue-rotate({turn}deg); }}
[data-testid="stTabs"] [role="tablist"] button p {{ color: {t["text"]}; font-weight: 700; filter: hue-rotate({-turn}deg); letter-spacing: 0.08em; }}

/* ---------- photos ---------- */
[data-testid="stImage"] img {{ {photo_css(t["photo_style"], t["card_border"], t["card_border"])} }}
[data-testid="stImageCaption"] p, [data-testid="stImageCaption"] [data-testid="stCaptionContainer"] p {{ font-size: 0.82rem; }}
.st-key-closet-grid {{ padding: 2.5rem 6vw 2rem 6vw; }}
.st-key-footer-bar {{ padding: 1.5rem 6vw 0 6vw; }}
[class*="st-key-rate-"] button {{ padding: 0.4rem 1.2rem !important; min-width: 0; }}
.st-key-questions-wrap {{ padding: 0 6vw 3rem 6vw; }}
{preview_css(previews) if previews else ""}
</style>
"""


def apply_theme(theme, previews=None):
    """Hand one vibe to Streamlit."""
    st.markdown(build_css(theme, previews), unsafe_allow_html=True)


def landing_css():
    """Extra CSS for the first page only: graph paper wallpaper over the whole page,
    a pink spiral behind the title, and cream cards with a red border for the vibes. All edges are straight."""
    spiral = "data:image/svg+xml;utf8," + quote(spiral_svg(SPIRAL_LIGHT, SPIRAL_DARK))
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Caprasimo&display=swap');
[data-testid="stMainBlockContainer"] {{ padding-bottom: 0 !important; }}

/* wallpaper: cream with thin pink lines going across and down, behind everything */
.stApp {{
    background-color: {CREAM} !important;
    background-image:
        linear-gradient({PINK_LINES} 1px, transparent 1px),
        linear-gradient(90deg, {PINK_LINES} 1px, transparent 1px) !important;
    background-size: 38px 38px !important;
    background-attachment: scroll !important;
}}

/* top: the pink spiral, everything centred */
.st-key-landing-top {{
    padding: 0 6vw 6rem 6vw; align-items: center; text-align: center;
    background: url("{spiral}") center / cover no-repeat;
}}
.st-key-landing-top [data-testid="stElementContainer"] {{ width: 100%; }}
.st-key-landing-top [data-testid="stMarkdownContainer"] {{ text-align: center; }}
.st-key-landing-top .nav {{ padding-left: 0; padding-right: 0; color: {RED}; }}
.st-key-landing-top .nav .logo {{ color: {RED}; }}
.stApp .st-key-landing-top p.eyebrow {{ color: {RED}; font-weight: 700; margin: 2.6rem 0 1.4rem 0; }}
.stApp .st-key-landing-top h1.mega {{
    color: {RED}; font-size: clamp(4rem, 11vw, 9.5rem) !important; margin-bottom: 1.6rem !important;
}}
.stApp .st-key-landing-top h1.mega .dot {{ color: {BUTTER}; }}
.stApp .st-key-landing-top p.lede {{ color: {RED}; max-width: 34rem; margin: 0 auto; font-size: 1.2rem; font-weight: 500; }}

/* bottom: the title label and the vibe cards sit straight on the wallpaper */
.st-key-vibes {{ padding: 4.5rem 6vw 5rem 6vw; }}
.st-key-vibes [data-testid="stMarkdownContainer"]:has(.section-title) {{ text-align: center; margin-bottom: 2.4rem; }}
.stApp .st-key-vibes h2.section-title {{
    display: inline-block; background: {CREAM}; color: {RED};
    border: 2px solid {RED}; padding: 0.4rem 1.6rem 0.5rem 1.6rem;
    border-radius: 999px; transform: rotate(-1.5deg); margin: 0;
    font-family: 'Caprasimo', serif; font-weight: 400;
    font-size: clamp(1.3rem, 2.2vw, 1.9rem) !important;
}}

/* the cards: the same cream as the wallpaper, with a red border and red writing */
.stApp .st-key-vibes [class*="st-key-vibe-"] {{ background: {CREAM} !important; background-image: none !important; border-color: {RED} !important; }}
.stApp .st-key-vibes .vibe-text b, .stApp .st-key-vibes .vibe-text small {{ color: {RED} !important; }}
.stApp .st-key-vibes .stButton > button {{ background: {RED} !important; border-color: {RED} !important; }}
.stApp .st-key-vibes .stButton > button p {{ color: {CREAM} !important; }}
</style>
"""
