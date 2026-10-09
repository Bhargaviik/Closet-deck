import pandas as pd
from engine import layers_for, filter_by_weather

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})

print("Layers at 5 degrees:", layers_for(5))
print("Layers at 25 degrees:", layers_for(25))

print("\nShoes on a DRY cold day:")
dry = filter_by_weather(catalogue, 5, is_raining=False)
print(dry[dry["slot"] == "shoes"])

print("\nShoes on a RAINY cold day:")
wet = filter_by_weather(catalogue, 5, is_raining=True)
print(wet[wet["slot"] == "shoes"])
