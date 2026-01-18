import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="Elite Athlete Pro", page_icon="🔥", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    div[data-testid="stMetricValue"] { color: #00ffcc; font-size: 32px; }
    .stButton>button { background-color: #00ffcc; color: black; border-radius: 20px; font-weight: bold; }
    .meal-card { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'weight' not in st.session_state: st.session_state.weight = []
if 'water' not in st.session_state: st.session_state.water = 0
if 'photos' not in st.session_state: st.session_state.photos = {}

# --- CALCULATOR ---
def get_athlete_specs(w, h, a, g, act, goal):
    bmr = (10*w) + (6.25*h) - (5*a) + (5 if g=="Male" else -161)
    tdee = bmr * act
    if goal == "Fat Loss":
        target = tdee - 500
    elif goal == "Muscle Gain":
        target = tdee + 300
    else:
        target = tdee
    
    # Athlete Protein: ~2.2g per kg
    prot_g = w * 2.2
    fats_g = (target * 0.25) / 9
    carbs_g = (target - (prot_g*4) - (fats_g*9)) / 4
    return round(target), round(prot_g), round(carbs_g), round(fats_g)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ COMMAND CENTER")
    name = st.text_input("Athlete Name", "Arjun")
    g = st.radio("Gender", ["Male", "Female"])
    w = st.number_input("Weight (kg)", 40, 150, 80)
    h = st.number_input("Height (cm)", 140, 210, 180)
    a = st.number_input("Age", 16, 60, 24)
    goal = st.selectbox("Current Mission", ["Fat Loss", "Maintenance", "Muscle Gain"])
    act = st.select_slider("Intensity Level", options=[1.2, 1.375, 1.55, 1.725, 1.9])
    mode = st.radio("Equipment", ["Commercial Gym", "Home/Minimalist"])

cals, prot, carb, fat = get_athlete_specs(w, h, a, g, act, goal)

# --- MAIN DASHBOARD ---
st.title(f"⚡ Athlete Dashboard: {name}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Daily Fuel", f"{cals} kcal")
m2.metric("Protein", f"{prot}g")
m3.metric("Carbs", f"{carb}g")
m4.metric("Fats", f"{fat}g")

tab_meal, tab_train, tab_progress, tab_science = st.tabs(["🍱 Nutrition", "🏋️ Training", "📸 Progress Tracker", "🧬 Science"])

with tab_meal:
    st.subheader("Indian Athlete Meal Plan")
    c_a, c_b = st.columns(2)
    with c_a:
        st.markdown('<div class="meal-card"><b>Breakfast:</b> 100g Paneer/Chicken + 2 Rotis + Curd</div>', unsafe_allow_html=True)
        st.markdown('<div class="meal-card"><b>Lunch:</b> 1.5 cup Dal + 1 cup Brown Rice + Large Salad</div>', unsafe_allow_html=True)
    with c_b:
        st.markdown('<div class="meal-card"><b>Snack:</b> Soya Chunks (50g) + 1 Fruit</div>', unsafe_allow_html=True)
        st.markdown('<div class="meal-card"><b>Dinner:</b> Grilled Fish/Dal Chilla + Stir-fry Veggies</div>', unsafe_allow_html=True)

with tab_train:
    st.subheader(f"7-Day {mode} Protocol")
    col_name = "Gym Exercises" if "Gym" in mode else "Home Exercises"
    plan = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Focus": ["Push", "Pull", "Legs", "Rest", "Upper", "HIIT", "Rest"],
        "Gym Exercises": ["Bench Press, Military Press", "Deadlifts, Rows", "Squats, Leg Press", "Mobility", "Incline DB, Pullups", "Sprints", "Recovery"],
        "Home Exercises": ["Diamond Pushups", "Inverted Rows", "Split Squats", "Yoga", "Regular Pushups", "Burpees", "Recovery"]
    }
    st.table(pd.DataFrame(plan)[['Day', 'Focus', col_name]])

with tab_progress:
    st.subheader("Body Transformation Gallery")
    # Weight Plot
    new_w = st.number_input("Log Today's Weight", 40.0, 150.0, float(w))
    if st.button("Save Weight Entry"):
        st.session_state.weight.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Weight": new_w})
    
    if st.session_state.weight:
        st.line_chart(pd.DataFrame(st.session_state.weight).set_index("Date"))

    # Photo Upload
    st.divider()
