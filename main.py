import pandas as pd
import opendatasets as od
from diseases_tracker import analyze_food_safety, suggest_alternatives
from recipe_generator import generate_healthy_recipe
import os
import sys

# Step 1: Download dataset (if not already present)

print("Downloading datasets (if not present)...")
dataset_url = "https://www.kaggle.com/datasets/stoicstatic/fooddata-central-nutrition-and-component-data"
dataset_path = "fooddata-central-nutrition-and-component-data"

try:
    od.download(dataset_url)
except Exception as e:
    print(f"⚠️ Dataset download skipped or failed: {e}")

if not os.path.exists(dataset_path):
    print("❌ Dataset folder not found. Exiting.")
    sys.exit(1)


# Step 2: Load and merge datasets

print("Merging datasets...")

food_df = pd.read_csv(os.path.join(dataset_path, "food.csv"), low_memory=False)
food_nutrient_df = pd.read_csv(os.path.join(dataset_path, "food_nutrient.csv"), low_memory=False)
nutrient_df = pd.read_csv(os.path.join(dataset_path, "nutrient.csv"), low_memory=False)

# Normalize column names
food_df.columns = food_df.columns.str.strip().str.lower()
food_nutrient_df.columns = food_nutrient_df.columns.str.strip().str.lower()
nutrient_df.columns = nutrient_df.columns.str.strip().str.lower()

# Validate join keys
if "fdc_id" not in food_nutrient_df.columns:
    raise KeyError("Missing 'fdc_id' column in food_nutrient.csv")

nutrient_key = None
for key in ["nutrient_id", "id", "nutrientid"]:
    if key in nutrient_df.columns:
        nutrient_key = key
        break

if not nutrient_key:
    raise KeyError("No valid nutrient ID column found in nutrient.csv")

# Merge datasets safely
merged_df = pd.merge(food_nutrient_df, nutrient_df, left_on="nutrient_id", right_on=nutrient_key, how="left")
merged_df.rename(columns={
    "name": "nutrient_name",
    "amount": "nutrient_amount"
}, inplace=True)

master_df = pd.merge(merged_df, food_df, on="fdc_id", how="left")

print("Master dataset ready ✅")


# Step 3: Main Program Interaction

print("\nWelcome to the Nutrition Analyser! 📊\n")

condition = input("Do you have any health condition? (Diabetes, Hypertension, Obesity, Heart Disease, None): ").strip()
food_name = input("Enter the grocery item you want to analyze (e.g., Milk, Bread, Ghee, Peanut Butter, Shahi Paneer, Pav Bhaji): ").strip()

# Find matching items
matches = master_df[master_df["description"].str.contains(food_name, case=False, na=False)]["description"].unique()

if len(matches) == 0:
    print("❌ No matching items found. Please try again.")
    sys.exit(0)

print("\nI found multiple items. Please choose one:")
for i, item in enumerate(matches[:10], start=1):
    print(f"{i}. {item}")

# Safe user input
while True:
    try:
        choice = int(input("\nEnter the number of your choice: "))
        if 1 <= choice <= len(matches[:10]):
            break
        else:
            print("❌ Invalid number. Try again.")
    except ValueError:
        print("❌ Please enter a valid number.")

selected_food = matches[choice - 1]


# Step 4: Nutrient Extraction

food_data = master_df[master_df["description"] == selected_food]

if food_data.empty:
    print("⚠️ No data found for the selected food.")
    sys.exit(0)

expected_cols = ["nutrient_name", "nutrient_amount", "unit_name"]
for col in expected_cols:
    if col not in food_data.columns:
        print(f"⚠️ Missing column in dataset: {col}")
        sys.exit(0)

nutrients = food_data[expected_cols].drop_duplicates()

print("\n--- Nutritional Report ---")
print(f"Product: {selected_food}")
print("Serving Size: Not specified (usually per 100 g)")
print("-------------------------")
for _, row in nutrients.iterrows():
    print(f"{row['nutrient_name']:<35}: {row['nutrient_amount']:.2f} {row['unit_name']}")


# Step 5: Health Check

print("\n--- Health Safety Check ---")
result, safe = analyze_food_safety(condition, nutrients)
print(result)


# Step 6: Recommendations

print("\n--- Recommended Alternatives ---")
suggestion = suggest_alternatives(condition)
print(suggestion)


# Step 7: Healthy Recipe Generation

print("\n--- Healthy Homemade Recipe Suggestion 🍲 ---")

# Extract homemade option from suggestion
if "🍴 Healthy Homemade Option:" in suggestion:
    homemade_option = suggestion.split("🍴 Healthy Homemade Option:")[1].strip()
else:
    homemade_option = "a healthy balanced meal"

recipe = generate_healthy_recipe(homemade_option, condition)
print(recipe)


# Step 8: Save Report
output_file = "nutrition_report.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"Product: {selected_food}\n\n{result}\n\n{suggestion}\n\n{recipe}")

