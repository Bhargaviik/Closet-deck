from itertools import product

# ---------- constants (lookup tables) ----------
RAIN_BOOTS = "rain boots"   # the words we search for in the name
SKIRT_WORDS = ["skirt"]                  # a bottom with one of these words is a skirt
LEGWEAR_WORDS = ["leggings", "tights"]   # ...and these go underneath a skirt

SEASONS_FOR_WEATHER = {
    "cold": ["winter", "all"],
    "cool": ["winter", "all"],
    "mild": ["all"],
    "warm": ["summer", "all"],
    "hot":  ["summer", "all"],
}

# Up to 20 degrees we layer: something on top of the top.
LAYERS_FOR_WEATHER = {
    "cold": ["base", "mid", "outer"],
    "cool": ["base", "outer"],
    "mild": ["base", "outer"],
    "warm": ["base"],
    "hot":  ["base"],
}

DRESS_WORDS = ["dress"]                  # a dress is a top and a bottom in one piece
PATTERN_WORDS = ["printed", "print", "floral", "plaid", "check", "striped", "paisley",
                 "polka", "suzani", "lace", "mesh"]   # busy pieces: do not wear two together

# Two pieces with the same word in the name are too alike (a hoodie under a hoodie).
SAME_KIND_WORDS = ["hoodie", "zip", "turtleneck", "mock-neck", "fleece", "cardigan", "vest", "jacket"]

# A top for this weather must be at least this warm (warmth column: 1 = light, 3 = very warm).
MIN_BASE_WARMTH = {"cold": 2, "cool": 2, "mild": 1, "warm": 1, "hot": 1}
# How warm the whole outfit should be on average.
TARGET_WARMTH = {"cold": 2.6, "cool": 2.2, "mild": 1.8, "warm": 1.3, "hot": 1.0}

# In these kinds of weather a skirt gets leggings or tights underneath.
LEGWEAR_WEATHER = ["cold", "cool", "mild"]

# Mid layers and coats do not have to match the occasion exactly:
# you can put any coat over a party outfit.
LAYER_SLOTS = ["mid", "outer"]
SLOT_NAMES = {"mid": "mid layers", "outer": "jackets and coats"}


# ---------- functions ----------
def weather_from_temperature(temp_c):
    """Turn a number like 25 into a word like 'warm'."""
    if temp_c < 8:
        return "cold"
    elif temp_c < 16:
        return "cool"
    elif temp_c <= 20:
        return "mild"
    elif temp_c <= 27:
        return "warm"
    else:
        return "hot"


def layers_for(temp_c, upper_layers=None, extra_layer=False):
    """Which slots do we need to fill at this temperature?

    upper_layers: None = let the weather decide, 1 = just a top,
    2 = a top plus a mid layer. The jacket or coat is decided by the weather.
    """
    weather = weather_from_temperature(temp_c)
    slots = list(LAYERS_FOR_WEATHER[weather])

    if upper_layers is None:
        wants_mid = extra_layer or "mid" in slots
    else:
        wants_mid = upper_layers >= 2

    if wants_mid and "mid" not in slots:
        slots.insert(1, "mid")      # base, mid, then the outer layer
    if not wants_mid and "mid" in slots:
        slots.remove("mid")
    return slots


def is_skirt(name):
    return any(word in name for word in SKIRT_WORDS)


def is_legwear(name):
    return any(word in name for word in LEGWEAR_WORDS)


def is_dress(name):
    return any(word in name for word in DRESS_WORDS)


def is_patterned(name):
    return any(word in name for word in PATTERN_WORDS)


def filter_by_occasion(catalogue, occasion):
    return catalogue[catalogue[occasion] == 1]


def filter_by_weather(catalogue, temp_c, is_raining=False):
    weather = weather_from_temperature(temp_c)
    allowed = SEASONS_FOR_WEATHER[weather]
    result = catalogue[catalogue["season"].isin(allowed)]

    if not is_raining:
        # dry day: hide the rain boots
        is_boots = result["name"].str.contains(RAIN_BOOTS)
        result = result[~is_boots]

    return result


def candidates_for_slot(catalogue, slot, occasion, is_raining, notes=None):
    """All items that could fill ONE slot (e.g. 'shoes').

    notes is an optional list: if we have to bend a rule, we add a sentence to it.
    """
    in_slot = catalogue[catalogue["slot"] == slot]
    is_boots = in_slot["name"].str.contains(RAIN_BOOTS)

    if slot == "shoes" and is_raining and is_boots.any():
        return in_slot[is_boots]         # rain: shoes must be rain boots

    matching = filter_by_occasion(in_slot[~is_boots], occasion)

    if matching.empty and slot in LAYER_SLOTS and not in_slot[~is_boots].empty:
        # nothing is labelled for this occasion, so use any piece from the slot
        if notes is not None:
            notes.append(f"None of your {SLOT_NAMES[slot]} is labelled '{occasion}', "
                         f"so I picked from all of them.")
        return in_slot[~is_boots]

    return matching


def build_outfits(catalogue, temp_c, occasion, is_raining=False, extra_layer=False,
                  upper_layers=None, notes=None):
    """Returns (list of outfits, name of a slot with no items or None)."""
    available = filter_by_weather(catalogue, temp_c, is_raining)
    weather = weather_from_temperature(temp_c)

    slots = layers_for(temp_c, upper_layers, extra_layer)
    slots = slots + ["bottom", "shoes"]

    used_slots = []
    options = []
    for slot in slots:
        if slot not in catalogue["slot"].values:
            continue

        found = candidates_for_slot(available, slot, occasion, is_raining, notes)
        if slot == "base" and "warmth" in found.columns:
            # no tank tops in the cold: keep tops that are warm enough for the weather
            warm_enough = found[found["warmth"] >= MIN_BASE_WARMTH[weather]]
            if not warm_enough.empty:
                found = warm_enough
        if slot == "bottom":
            # leggings and tights are underwear for skirts, never the bottom on their own
            found = found[~found["name"].apply(is_legwear)]
        if found.empty:
            return [], slot
        used_slots.append(slot)
        options.append(found["name"].tolist())

    combos = list(product(*options))

    bottoms = available[available["slot"] == "bottom"]
    legwear = [name for name in bottoms["name"] if is_legwear(name)]
    wants_legwear = weather in LEGWEAR_WEATHER and bool(legwear)

    if "base" not in used_slots or "bottom" not in used_slots:
        return combos, None

    base_at = used_slots.index("base")
    bottom_at = used_slots.index("bottom")

    outfits = []
    seen = set()
    for combo in combos:
        base, bottom = combo[base_at], combo[bottom_at]
        if is_dress(base):
            # a dress already is the bottom: drop the extra bottom, add tights if it is cold
            without = tuple(n for i, n in enumerate(combo) if i != bottom_at)
            variants = [without + (t,) for t in legwear] if wants_legwear else [without]
        elif is_skirt(bottom) and wants_legwear:
            variants = [combo + (t,) for t in legwear]
        else:
            variants = [combo]
        for variant in variants:
            if variant not in seen:
                seen.add(variant)
                outfits.append(variant)
    return outfits, None


NEUTRALS = ["black", "white", "grey", "beige", "navy", "denim"]


def colour_score(colours):
    """Fewer bright colours = better. 3 points max."""
    bright = set(c for c in colours if c not in NEUTRALS)
    return max(0, 3 - len(bright))


def score_outfit(outfit, info, style, preferred_color=None, weather=None):
    """Give one outfit (a tuple of item names) a score.

    info is a lookup table made once in rank_outfits:
    {item name: {"formality": 2, "color": "black", "warmth": 2}}
    """
    formalities = [info[name]["formality"] for name in outfit]
    colours = [info[name]["color"] for name in outfit]

    avg_formality = sum(formalities) / len(formalities)
    style_points = 3 - abs(avg_formality - style)

    colour_points = colour_score(colours)

    like_points = 0
    if preferred_color is not None:
        like_points = colours.count(preferred_color)

    # fashion sense 1: the pieces should be about equally dressy
    spread = max(formalities) - min(formalities)
    spread_points = -1.0 * max(0, spread - 1)

    # fashion sense 2: at most one busy (patterned) piece
    busy = sum(1 for name in outfit if is_patterned(name))
    busy_points = -1.5 * max(0, busy - 1)

    # fashion sense 3: no two pieces of the same kind (a hoodie on a hoodie)
    twins = sum(1 for word in SAME_KIND_WORDS if sum(word in name for name in outfit) > 1)
    twin_points = -2.0 * twins

    # fashion sense 4: warm enough (or cool enough) for the weather
    warmth_points = 0
    if weather is not None:
        warmths = [info[name]["warmth"] for name in outfit]
        warmth_points = -1.0 * abs(sum(warmths) / len(warmths) - TARGET_WARMTH[weather])

    return style_points + colour_points + like_points + spread_points + busy_points + twin_points + warmth_points


def rank_outfits(outfits, catalogue, style, preferred_color=None, top=3, temp_c=None, skip=0):
    """Score every outfit and return the best ones.

    The top outfits all start with a different top, so you do not get three
    copies of the same outfit. skip=1 gives the next round of suggestions.
    """
    weather = weather_from_temperature(temp_c) if temp_c is not None else None
    # look the items up once instead of searching the table for every outfit
    info = catalogue.set_index("name")[["formality", "color", "warmth"]].to_dict("index")

    scored = []
    for outfit in outfits:
        points = score_outfit(outfit, info, style, preferred_color, weather)
        scored.append((points, outfit))
    scored.sort(key=lambda pair: pair[0], reverse=True)

    chosen, used_tops = [], set()
    for points, outfit in scored:
        if outfit[0] not in used_tops:
            chosen.append((points, outfit))
            used_tops.add(outfit[0])
    # if there are fewer different tops than we need, fill up with the next best
    for pair in scored:
        if len(chosen) >= (skip + 1) * top:
            break
        if pair not in chosen:
            chosen.append(pair)
    return chosen[skip * top: skip * top + top]
