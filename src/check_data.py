import pandas as pd

catalogue = pd.read_csv("data/catalogue.csv", dtype={"id": str})

OCCASIONS = ["daily", "formal", "party", "date", "sport"]

print(len(catalogue), "items\n")
print(catalogue["slot"].value_counts(), "\n")
print(catalogue[OCCASIONS].sum(), "\n")
print("Items with no occasion:", (catalogue[OCCASIONS].sum(axis=1) == 0).sum())
print("Empty cells:\n", catalogue.isna().sum())
print("Duplicate names:", catalogue["name"].duplicated().sum())