# recipe_generator.py
import google.generativeai as gem

# Configure your Gemini API
gem.configure(api_key="AIzaSyAHZBpFJA9p_vtlJN7ZhZdou97SlOagbmQ")

# Load model
model = gem.GenerativeModel('gemini-2.0-flash')

def generate_healthy_recipe(food_name, disease):
    """
    Uses Gemini LLM to suggest a healthy homemade recipe
    adapted for a specific disease or condition.
    """
    query = (
        f"Suggest a healthy homemade recipe using {food_name}. "
        f"It should be safe and beneficial for a person with {disease}. "
        "Include ingredients, preparation steps, and nutritional benefits briefly."
    )

    try:
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f" Could not generate recipe: {e}"
