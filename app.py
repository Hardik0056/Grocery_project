import streamlit as st
import pandas as pd
import opendatasets as od
import os
import time

from diseases_tracker import analyze_food_safety, suggest_alternatives
from recipe_generator import generate_healthy_recipe

st.set_page_config(page_title="Grocery Insights Analyzer", page_icon="🛒", layout="wide")

if "data_loaded" not in st.session_state:
    with st.spinner("⏳ Initializing Application...\nLoading dataset, merging files, preparing system..."):
        time.sleep(1)

        dataset_url = "https://www.kaggle.com/datasets/stoicstatic/fooddata-central-nutrition-and-component-data"
        dataset_path = "fooddata-central-nutrition-and-component-data"

        try:
            od.download(dataset_url)
        except Exception as e:
            st.warning(f"Dataset download skipped or failed: {e}")

        if not os.path.exists(dataset_path):
            st.error("❌ Dataset not found. Cannot continue.")
            st.stop()

        # Load CSV files
        food_df = pd.read_csv(os.path.join(dataset_path, "food.csv"), low_memory=False)
        food_nutrient_df = pd.read_csv(os.path.join(dataset_path, "food_nutrient.csv"), low_memory=False)
        nutrient_df = pd.read_csv(os.path.join(dataset_path, "nutrient.csv"), low_memory=False)

        # Normalize
        food_df.columns = food_df.columns.str.strip().str.lower()
        food_nutrient_df.columns = food_nutrient_df.columns.str.strip().str.lower()
        nutrient_df.columns = nutrient_df.columns.str.strip().str.lower()

        # Merge datasets
        nutrient_key = "id" if "id" in nutrient_df.columns else "nutrient_id"

        merged_df = pd.merge(
            food_nutrient_df, nutrient_df,
            left_on="nutrient_id",
            right_on=nutrient_key, how="left"
        )
        merged_df.rename(columns={
            "name": "nutrient_name",
            "amount": "nutrient_amount"
        }, inplace=True)

        master_df = pd.merge(merged_df, food_df, on="fdc_id", how="left")
        st.session_state["master_df"] = master_df

        time.sleep(1)

    st.session_state["data_loaded"] = True
    st.success("🚀 App Loaded Successfully!")

st.title("🛒 Grocery Insights Analyzer")
st.write("Analyze food items, health impact, alternatives & healthy recipes.")

master_df = st.session_state["master_df"]


st.header("🔎 Search Food")

condition = st.selectbox(
    "Select your health condition:",
    ["None", "Diabetes", "Hypertension", "Obesity", "Heart Disease"]
)

food_name = st.text_input("Enter the grocery item (e.g., Milk, Bread, Ghee):")

if st.button("Find Matches"):
    matches = master_df[
        master_df["description"].str.contains(food_name, case=False, na=False)
    ]["description"].unique()

    if len(matches) == 0:
        st.error("❌ No matching items found.")
        st.stop()

    st.session_state["matches"] = matches[:10]
    st.success("Items found!")


if "matches" in st.session_state:
    selected_food = st.selectbox("Select the exact item:", st.session_state["matches"])

    if st.button("Analyze"):
        data = master_df[master_df["description"] == selected_food]

        if data.empty:
            st.error("❌ No data for selected food.")
            st.stop()

        nutrients = data[["nutrient_name", "nutrient_amount", "unit_name"]].drop_duplicates()

        # NUTRITION
        st.header("📊 Nutritional Report")
        st.subheader(selected_food)
        st.dataframe(nutrients)

        # HEALTH CHECK
        st.header("🩺 Health Safety Check")
        result, is_safe = analyze_food_safety(condition, nutrients)
        st.write(result)

        # ALTERNATIVES
        st.header("🔄 Recommended Alternatives")
        suggestion = suggest_alternatives(condition)
        st.write(suggestion)

        # RECIPE (Gemini)
        st.header("🍲 Healthy Recipe Suggestion")
        if "🍴 Healthy Homemade Option:" in suggestion:
            homemade_option = suggestion.split("🍴 Healthy Homemade Option:")[1].strip()
        else:
            homemade_option = selected_food

        recipe = generate_healthy_recipe(homemade_option, condition)
        st.write(recipe)

        # SAVE REPORT
        output = f"""
Product: {selected_food}

{result}

{suggestion}

{recipe}
"""
        with open("nutrition_report.txt", "w", encoding="utf-8") as f:
            f.write(output)

        st.success("📄 Report saved as nutrition_report.txt")
