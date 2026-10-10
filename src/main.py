import pandas as pd
from engine import build_outfits, rank_outfits

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})

OCCASIONS = ["daily", "formal", "party", "date"]


def ask(question, default):
    """Ask one question. Pressing Enter skips it and uses the default."""
    answer = input(f"{question} [Enter = {default}]: ").strip()
    if answer == "":
        return default
    return answer


def ask_number(question, default):
    answer = ask(question, default)
    try:
        return float(answer)
    except ValueError:
        print("That wasn't a number, using", default)
        return default


def ask_yes_no(question, default="n"):
    return ask(question + " (y/n)", default).lower().startswith("y")


print("Pearlfect - answer 5 questions (press Enter to skip any)\n")

temp_c = ask_number("1. Temperature in degrees C", 18)
is_raining = ask_yes_no("   Is it raining?")

occasion = ask("2. Occasion " + str(OCCASIONS), "daily").lower()
if occasion not in OCCASIONS:
    print("Unknown occasion, using daily")
    occasion = "daily"

style = ask_number("3. Style: 1 = comfy ... 3 = formal", 2)
extra_layer = ask_yes_no("4. Do you want an extra layer?")

colour = ask("5. Favourite colour (or 'none')", "none").lower()
if colour == "none":
    colour = None

outfits, missing = build_outfits(catalogue, temp_c, occasion, is_raining, extra_layer)

print()
if missing:
    print("Sorry, no items for slot:", missing)
else:
    print(f"{len(outfits)} possible outfits. Top 3:")
    for points, outfit in rank_outfits(outfits, catalogue, style, colour):
        print(round(points, 2), outfit)