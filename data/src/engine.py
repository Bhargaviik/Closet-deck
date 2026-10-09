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