import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("Dataset .csv")

# Normalize column names
df.columns = df.columns.str.strip()

# Map detected columns
cuisine_col = "Cuisines"
city_col = "City"
rating_col = "Aggregate rating"
price_col = "Average Cost for two"
online_col = "Has Online delivery"

# -----------------------------
# LEVEL 1 – TASK 1 : Top Cuisines
# -----------------------------
print("\n--- LEVEL 1 : TASK 1 — Top Cuisines ---")

# Split cuisines (comma / pipe)
cuisines = (
    df[cuisine_col]
    .fillna("")
    .astype(str)
    .str.split(r",|\|")
    .explode()
    .str.strip()
)
cuisines = cuisines[cuisines != ""]

cuisine_counts = cuisines.value_counts()
total_restaurants = df.shape[0]

top3_cuisines = pd.DataFrame({
    "Cuisine": cuisine_counts.index[:3],
    "Count": cuisine_counts.values[:3],
    "Percentage(%)": (cuisine_counts.values[:3] / total_restaurants * 100).round(2)
})

print(top3_cuisines)

# -----------------------------
# LEVEL 1 – TASK 2 : City Analysis
# -----------------------------
print("\n--- LEVEL 1 : TASK 2 — City Analysis ---")

# Count restaurants per city
city_counts = df[city_col].value_counts()

print("\nCity with highest number of restaurants:")
print(city_counts.head(1))

# Rating per city
df["rating_numeric"] = pd.to_numeric(df[rating_col], errors="coerce")
avg_rating_city = df.groupby(city_col)["rating_numeric"].mean().round(2)

print("\nAverage rating per city (top 10):")
print(avg_rating_city.head(10))

# Highest avg rating city (with ≥3 restaurants)
city_rest_count = df[city_col].value_counts()
eligible = city_rest_count[city_rest_count >= 3].index

if len(eligible) > 0:
    city_highest_avg = avg_rating_city.loc[eligible].idxmax()
    highest_avg_value = avg_rating_city.loc[eligible].max()
else:
    city_highest_avg = avg_rating_city.idxmax()
    highest_avg_value = avg_rating_city.max()

print("\nCity with highest avg rating:")
print(city_highest_avg, highest_avg_value)

# -----------------------------
# LEVEL 1 – TASK 3 : Price Range Distribution
# -----------------------------
print("\n--- LEVEL 1 : TASK 3 — Price Range Distribution ---")

price_counts = df[price_col].value_counts().sort_index()
price_df = pd.DataFrame({
    "Price Range": price_counts.index,
    "Count": price_counts.values,
    "Percentage(%)": (price_counts.values / len(df) * 100).round(2)
})

print(price_df)

# Bar chart
plt.figure(figsize=(7,5))
plt.bar(price_df["Price Range"].astype(str), price_df["Count"])
plt.title("Price Range Distribution")
plt.xlabel("Price Range")
plt.ylabel("Restaurant Count")
plt.tight_layout()
plt.show()
# -----------------------------
# LEVEL 1 – TASK 4 : Online Delivery
# -----------------------------
print("\n--- LEVEL 1 : TASK 4 — Online Delivery ---")

# Normalize values
online_flag = df[online_col].astype(str).str.lower().isin(
    ["yes", "1", "true", "y"]
).astype(int)

pct_online = round((online_flag.sum() / len(df)) * 100, 2)

print("\nPercentage offering online delivery:", pct_online, "%")

# Compare ratings
rating_numeric = pd.to_numeric(df[rating_col], errors="coerce")

avg_with = rating_numeric[online_flag == 1].mean()
avg_without = rating_numeric[online_flag == 0].mean()

print("\nAverage rating WITH online delivery:", round(avg_with, 2))
print("Average rating WITHOUT online delivery:", round(avg_without, 2))
