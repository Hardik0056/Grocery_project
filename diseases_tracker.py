"""
diseases_tracker.py
-------------------
Analyzes whether a food is safe for a given health condition,
based on nutrient names, thresholds, and risk levels.
"""

import pandas as pd

# Disease-specific rules and quantitative thresholds
DISEASE_RULES = {
    "diabetes": {
        "avoid": {
            "Sugars, total including NLEA": (3, 6),  # g
        },
        "recommend": ["Whole Grains", "Vegetables"],
        "homemade": "Oats porridge with nuts"
    },
    "hypertension": {
        "avoid": {
            "Sodium, Na": (150, 400),  # mg
        },
        "recommend": ["Fruits", "Leafy greens"],
        "homemade": "Fresh vegetable salad with lemon dressing"
    },
    "obesity": {
        "avoid": {
            "Total lipid (fat)": (8, 15),  # g
            "Sugars, total including NLEA": (4, 8),  # g
        },
        "recommend": ["Lean protein", "Vegetables"],
        "homemade": "Grilled chicken with steamed veggies"
    },
    "heart disease": {
        "avoid": {
            "Total lipid (fat)": (6, 12),   # g
            "Sodium, Na": (150, 400),       # mg
            "Cholesterol": (40, 80),        # mg
        },
        "recommend": ["Oats", "Nuts", "Fish"],
        "homemade": "Steamed fish with spinach"
    },
}


def analyze_food_safety(disease, found_nutrients):
    """
    Check if a food item is safe for the given disease,
    and categorize nutrient levels into safe/moderate/high risk.
    """
    disease = disease.lower().strip()

    # Match plural forms or partial names
    for key in DISEASE_RULES.keys():
        if key in disease:
            disease = key
            break
    else:
        return "No rules found for this disease.", True

    rules = DISEASE_RULES[disease]
    avoid_rules = rules["avoid"]

    results = []
    overall_status = "safe"

    for nutrient_name, (safe_limit, moderate_limit) in avoid_rules.items():
        nutrient_row = found_nutrients[found_nutrients["nutrient_name"].str.lower() == nutrient_name.lower()]

        if not nutrient_row.empty:
            amount = nutrient_row["nutrient_amount"].values[0]

            # Determine risk level
            if amount <= safe_limit:
                results.append(f" {nutrient_name}: {amount:.2f} (Safe)")
            elif safe_limit < amount <= moderate_limit:
                results.append(f" {nutrient_name}: {amount:.2f} (Moderate risk for {disease.title()})")
                if overall_status == "safe":
                    overall_status = "moderate"
            else:
                results.append(f" {nutrient_name}: {amount:.2f} (High risk for {disease.title()})")
                overall_status = "unsafe"

    if not results:
        return f"No matching nutrients found for {disease.title()}.", True

    # Determine final verdict
    if overall_status == "safe":
        verdict = f" Safe to consume for {disease.title()}."
        is_safe = True
    elif overall_status == "moderate":
        verdict = f" Consume occasionally (moderate risk for {disease.title()})."
        is_safe = True
    else:
        verdict = f" Not safe to consume for {disease.title()}."
        is_safe = False

    report = "\n".join(results) + f"\n\n{verdict}"
    return f"--- Health Safety Check ---\n{report}", is_safe


def suggest_alternatives(disease):
    """Suggest safer food alternatives."""
    disease = disease.lower().strip()
    for key in DISEASE_RULES.keys():
        if key in disease:
            disease = key
            break
    else:
        return "No suggestions available."

    rules = DISEASE_RULES[disease]
    return (
        f"Recommended foods: {', '.join(rules['recommend'])}\n"
        f"🍴 Healthy Homemade Option: {rules['homemade']}"
    )
