from itertools import product
# ---------- constants (lookup tables) ----------
RAIN_BOOTS = "rain boots"   # the words we search for in the name

SEASONS_FOR_WEATHER = {
    "cold": ["winter", "all"],
    "cool": ["winter", "all"],
    "mild": ["all"],
    "warm": ["summer", "all"],
    "hot":  ["summer", "all"],
}

LAYERS_FOR_WEATHER = {
    "cold": ["base", "mid", "outer"],
    "cool": ["base", "outer"],
    "mild": ["base"],
    "warm": ["base"],
    "hot":  ["base"],
}


# ---------- functions ----------
def weather_from_temperature(temp_c):
    """Turn a number like 25 into a word like 'warm'."""
    if temp_c < 8:
        return "cold"
    elif temp_c < 16:
        return "cool"
    elif temp_c < 23:
        return "mild"
    elif temp_c <= 27:
        return "warm"
    else:
        return "hot"


def layers_for(temp_c):
    """Which slots do we need to fill at this temperature?"""
    weather = weather_from_temperature(temp_c)
    return LAYERS_FOR_WEATHER[weather]


def filter_by_occasion(catalogue, occasion):
    return catalogue[catalogue["occasion"] == occasion]


def filter_by_weather(catalogue, temp_c, is_raining=False):
    weather = weather_from_temperature(temp_c)
    allowed = SEASONS_FOR_WEATHER[weather]
    result = catalogue[catalogue["season"].isin(allowed)]

    if not is_raining:
        # dry day: hide the rain boots
        is_boots = result["name"].str.contains(RAIN_BOOTS)
        result = result[~is_boots]

    return result
def candidates_for_slot(catalogue, slot, occasion, is_raining):
    """All items that could fill ONE slot (e.g. 'shoes')."""
    in_slot = catalogue[catalogue["slot"] == slot]
    is_boots = in_slot["name"].str.contains(RAIN_BOOTS)

    if slot == "shoes" and is_raining:
        return in_slot[is_boots]          # rain: shoes must be rain boots

    return filter_by_occasion(in_slot[~is_boots], occasion)


def build_outfits(catalogue, temp_c, occasion, is_raining=False, extra_layer=False):
    """Returns (list of outfits, name of a slot with no items or None)."""
    available = filter_by_weather(catalogue, temp_c, is_raining)
    slots = layers_for(temp_c)
    if extra_layer and "mid" not in slots:
        slots = slots[:1] + ["mid"] + slots[1:]
    slots = slots + ["bottom", "shoes"]

    options = []
    for slot in slots:
        found = candidates_for_slot(available, slot, occasion, is_raining)
        if found.empty:
            return [], slot               # stop: nothing for this slot
        options.append(found["name"].tolist())

    return list(product(*options)), None

NEUTRALS = ["black", "white", "grey", "beige", "navy", "denim"]


def colour_score(colours):
    """Fewer bright colours = better. 3 points max."""
    bright = set(c for c in colours if c not in NEUTRALS)
    return max(0, 3 - len(bright))


def score_outfit(outfit, catalogue, style, preferred_color=None):
    """Give one outfit (a tuple of item names) a score."""
    items = catalogue.set_index("name").loc[list(outfit)]

    avg_formality = items["formality"].mean()
    style_points = 3 - abs(avg_formality - style)

    colour_points = colour_score(items["color"].tolist())

    like_points = 0
    if preferred_color is not None:
        like_points = (items["color"] == preferred_color).sum()

    return style_points + colour_points + like_points


def rank_outfits(outfits, catalogue, style, preferred_color=None, top=3):
    """Score every outfit and return the best ones."""
    scored = []
    for outfit in outfits:
        points = score_outfit(outfit, catalogue, style, preferred_color)
        scored.append((points, outfit))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return scored[:top]

