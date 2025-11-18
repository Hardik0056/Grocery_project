Here is the **exact clean text** you can directly paste into your **README.md** file.

---

# 🛒 Grocery / Products Insights Analyzer

### A Health-Based Food Analysis System using Streamlit & Python

The **Grocery/Products Insights Analyzer** is a Python–based web application built using **Streamlit** that analyzes packaged food and grocery items using nutritional information. It helps users make safer and healthier choices, especially those with health conditions like diabetes, hypertension, or obesity.

---

## ⭐ Features

### **1. Product Search**

Search any grocery or packaged food item and fetch its complete nutritional profile.

### **2. Nutritional Insights**

Displays:

* Calories
* Sugar
* Fat
* Protein
* Sodium
* Other nutritional components

### **3. Disease-Based Safety Analysis**

Rule-based analysis:

* Diabetes → Avoid high-sugar foods
* Hypertension → Avoid high-sodium foods
* Obesity → Avoid high-calorie or high-fat foods

Results shown as:

* ✔ Safe
* ⚠ Moderate
* ❌ Unsafe

### **4. Healthy Alternatives**

Suggests healthier substitute food items based on reduced sugar, sodium, calories, or fat.

### **5. AI Recipe Chatbot**

Generates:

* Healthy recipes
* Ingredient lists
* Personalized food recommendations

### **6. Streamlit Web Interface**

Interactive UI that updates results in real-time.

---

## 📂 Project Structure

```
app.py                     → Main Streamlit interface
diseases_tracker.py        → Disease rule engine
recipe_generator.py        → AI recipe generator logic
datasets/                  → Contains downloaded/merged data
README.md                  → Project documentation
```

---

## ⚙️ Technologies Used

* Python
* Pandas
* Streamlit
* Opendatasets
* Basic NLP for chatbot

---

## 🗂 Dataset Used

FoodData Central (Kaggle Dataset)
Automatically downloaded using **opendatasets**.

---

## 🚀 How to Run the Project

### Install dependencies:

```
pip install streamlit pandas opendatasets
```

### Run the Streamlit web app:

```
streamlit run app.py
```

The application will open at:

```
http://localhost:8501
```

---

## 🔄 Workflow

1. Download dataset using opendatasets.
2. Load and clean data with Pandas.
3. Merge all datasets into a unified DataFrame.
4. Launch Streamlit app.
5. User enters product name.
6. System performs case-insensitive matching.
7. Extracts nutritional values.
8. Applies disease-based rules.
9. Suggests healthier alternatives.
10. Recipe chatbot generates healthy recipes.
11. Display all insights in real-time.

---

## 🧠 Future Improvements

* ML-based nutrition prediction
* Barcode/QR scanning
* User login and saved history
* Mobile app version
* Advanced recipe generation

---

## 👤 Author

**Hardik**
CSE (AIFT), Semester 3
Chitkara University, Rajpura
Faculty: *Mr. Mudrik Kaushik*

---

