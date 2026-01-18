import streamlit as st
import pandas as pd
import random
from datetime import date
import os

# --- APP CONFIGURATION ---
st.set_page_config(page_title="BodyFuel Pro", page_icon="📈")

# --- FILE DATABASE LOGIC ---
DATA_FILE = "weight_history.csv"

def save_weight(w):
    new_data = pd.DataFrame([[date.today(), w]], columns=["Date", "Weight"])
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(DATA_FILE, index=False)

# --- 1. BIOMETRIC CALCULATOR ---
def get_nutrition(w, h, a, g, act, goal):
    bmr = (10 * w) + (6.25 * h) - (5 * a) + (5 if g == "Male" else -161)
    mult = {"Sedentary": 1.2, "Moderate": 1.55, "Active": 1.725}
    tdee = bmr * mult[act]
    if goal == "Lose Weight": tdee -= 500
    elif goal == "Build Muscle": tdee += 500
    return round(tdee), round(tdee*0.3/4), round(tdee*0.4/4), round(tdee*0.3/9)

# --- 2. USER INTERFACE ---
st.title("📈 BodyFuel Pro: Nutrition & Tracking")

tab1, tab2 = st.tabs(["Daily Plan", "Progress Tracker"])

with tab1:
    with st.sidebar:
        st.header("Body Biometrics")
        w = st.number_input("Current Weight (kg)", 40.0, 150.0, 75.0)
        h = st.number_input("Height (cm)", 120, 220, 175)
        a = st.number_input("Age", 15, 95, 30)
        g = st.selectbox("Gender", ["Male", "Female"])
        act = st.selectbox("Activity", ["Sedentary", "Moderate", "Active"])
        goal = st.selectbox("Goal", ["Maintain", "Lose Weight", "Build Muscle"])

    calories, prot, carb, fat = get_nutrition(w, h, a, g, act, goal)

    

    st.subheader("📊 Your Daily Targets")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calories", f"{calories}")
    c2.metric("Protein", f"{prot}g")
    c3.metric("Carbs", f"{carb}g")
    c4.metric("Fats", f"{fat}g")

    st.divider()
    if st.button("Generate Today's Meal Plan"):
        # (Meal generation logic same as previous version)
        st.success("Plan generated! Check the instructions below.")

with tab2:
    st.subheader("📉 Weight Progress Over Time")
    
    # Input for today's weight
    current_w = st.number_input("Log Today's Weight (kg)", 40.0, 150.0, w, key="log_w")
    if st.button("Save Weight Entry"):
        save_weight(current_w)
        st.balloons()
        st.success("Weight saved!")

    # Display the Chart
    if os.path.isfile(DATA_FILE):
        history_df = pd.read_csv(DATA_FILE)
        history_df['Date'] = pd.to_datetime(history_df['Date'])
        
        
        
        st.line_chart(history_df.set_index('Date'))
        st.dataframe(history_df.sort_values(by="Date", ascending=False))
    else:
        st.info("No data logged yet. Save your first entry to see the chart!")
