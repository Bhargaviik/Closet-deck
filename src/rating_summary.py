"""Prints the average rating from data/ratings.csv.

Run it from the project folder:  python src/rating_summary.py
"""

import pandas as pd

ratings = pd.read_csv("data/ratings.csv")
print(f"{len(ratings)} ratings, average {ratings['score'].mean():.2f} out of 5")
print()
print("By occasion:")
print(ratings.groupby("occasion")["score"].agg(["count", "mean"]).round(2))
print()
print("Cold (below 16 C) vs not cold:")
ratings["cold"] = ratings["temp_c"] < 16
print(ratings.groupby("cold")["score"].agg(["count", "mean"]).round(2))
print()
print("Worst rated looks:")
print(ratings.sort_values("score").head(5)[["temp_c", "occasion", "outfit", "score"]].to_string(index=False))
