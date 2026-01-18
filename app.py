import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# --- APP CONFIG ---
st.set_page_config(page_title="Elite Athlete Pro", page_icon="🔥", layout="wide")

# --- STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #e0e0e0; }
    div[data-testid="stMetricValue"] { color: #00ffcc; font-size: 32px; }
    .stButton>button { background-color: #00ffcc; color: black; width: 100%; border-radius: 20px; font-weight: bold; }
    .meal-card { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (DATABASE) ---
if 'logs' not in st.session_state: st.session_state.logs = []
if 'weight' not in st.session_state: st.session_state.weight = []
if 'water' not in st.session_state: st.session_state.water = 0

# --- CALCULATOR ---
def get_athlete_specs(w, h, a, g, act, goal):
    bmr = (10*w) + (6.25*h) - (5*a) + (5 if g=="Male" else -161)
    tdee = bmr * act
    target = tdee - 500 if goal=="Fat Loss" else (tdee + 300 if goal=="Muscle Gain" else tdee)
    # Athlete Protein: 2.2g per kg of bodyweight
    prot_g = w * 2.2
    fats_g = (target * 0.25) / 9
    carbs_g = (target - (prot_g*4) - (fats_g*9)) / 4
    return round(target), round(prot_g), round(carbs_g), round(fats_g)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ COMMAND CENTER")
    name = st.text_input("Athlete Name", "Arjun")
    g = st.radio("Biological Gender", ["Male", "Female"])
    w = st.number_input("Weight (kg)", 40, 150, 80)
    h = st.number_input("Height (cm)", 140, 210, 180)
    a = st.number_input("Age", 16, 60, 24)
    goal = st.selectbox("Current Mission", ["Fat Loss", "Maintenance", "Muscle Gain"])
    act = st.select_slider("Intensity Level", options=[1.2, 1.375, 1.55, 1.725, 1.9], help="1.9 is for Professional Athletes")
    mode = st.radio("Equipment Access", ["Commercial Gym", "Home/Minimalist"])

cals, prot, carb, fat = get_athlete_specs(w, h, a, g, act, goal)

# --- MAIN DASHBOARD ---
st.title(f"⚡ Athlete Dashboard: {name}")

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric("Daily Fuel", f"{cals} kcal")
m2.metric("Protein (Build)", f"{prot}g")
m3.metric("Carbs (Energy)", f"{carb}g")
m4.metric("Fats (Hormones)", f"{fat}g")

# --- FEATURES ---
tab_meal, tab_train, tab_search, tab_analytics = st.tabs(["🍱 Meal Timing", "🏋️ Workout Engine", "🔍 Indian Food DB", "📈 Performance Stats"])

with tab_meal:
    st.subheader("Timed Nutrition for Athletes")
    st.info("🕒 **Pre-Workout (2 hrs before):** High Carb + Low Fat (Oats/Banana/Toast)")
    st.success("🕒 **Post-Workout (Within 1 hr):** High Protein + Fast Carbs (Whey + Rice/Potatoes)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="meal-card"><b>Meal 1: High Protein Breakfast</b><br>4 Egg Whites + 1 Whole Egg + 2 Rotis or 100g Paneer + Soya Chunks</div>', unsafe_allow_html=True)
        st.markdown('<div class="meal-card"><b>Meal 2: Performance Lunch</b><br>150g Chicken/Paneer + 1 cup Dal + Salad + 1 cup Rice</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="meal-card"><b>Meal 3: Evening Recovery</b><br>Greek Yogurt + Berries or Roasted Chana + Whey Protein</div>', unsafe_allow_html=True)
        st.markdown('<div class="meal-card"><b>Meal 4: Anti-Inflammatory Dinner</b><br>Fish/Moong Dal + Steamed Veggies + Pinch of Turmeric</div>', unsafe_allow_html=True)

with tab_train:
    st.subheader(f"7-Day {mode} Protocol")
    plan = {
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "Focus": ["Push (Power)", "Pull (Strength)", "Legs (Mass)", "Recovery/Yoga", "Upper (Volume)", "HIIT/Explosive", "Full Rest"],
        "Gym Exercises": ["Bench 4x8, Military Press", "Deadlifts 3x5, Rows", "Squats 4x10, Leg Press", "Mobility Drills", "Incline DB, Pullups", "Sprints, Kettlebell", "Sleep & Eat"],
        "Home Exercises": ["Diamond Pushups, Pike Push", "Inverted Rows, Pullups", "Split Squats, Glute Bridge", "Yoga", "Regular Pushups, Dips", "Burpees, Mountain Climbers", "Sleep & Eat"]
    }
    df_plan = pd.DataFrame(plan)
    st.table(df_plan[['Day', 'Focus', f'{mode} Exercises']])
    
    

with tab_search:
    st.subheader("Indian Food Nutrient Lookup")
    food_db = {
        "Paneer (100g)": {"Cals": 265, "Prot": 18, "Carb": 1, "Fat": 20},
        "Chicken Breast (100g)": {"Cals": 165, "Prot": 31, "Carb": 0, "Fat": 3.6},
        "Moong Dal (1 cup)": {"Cals": 147, "Prot": 9, "Carb": 25, "Fat": 0.8},
        "Roti (1 medium)": {"Cals": 85, "Prot": 3, "Carb": 18, "Fat": 0.5},
        "Soya Chunks (50g)": {"Cals": 170, "Prot": 26, "Carb": 15, "Fat": 0.5},
    }
    search = st.selectbox("Select a common Indian food to check stats:", list(food_db.keys()))
    res = food_db[search]
    st.json(res)

with tab_analytics:
    st.subheader("Performance Tracking")
    c_l, c_r = st.columns(2)
    with c_l:
        wt = st.number_input("Log Today's Weight", 40.0, 150.0, float(w))
        if st.button("Log Weight"):
            st.session_state.weight.append({"Date": datetime.now().strftime("%Y-%m-%d"), "Weight": wt})
    
    if st.session_state.weight:
        df_w = pd.DataFrame(st.session_state.weight)
        st.line_chart(df_w.set_index("Date"))
    
    st.subheader("Hydration Logic")
    if st.button("Log 1 Litre"): st.session_state.water += 1
    st.write(f"Hydration: {st.session_state.water}/4 Litres")
    st.progress(min(st.session_state.water/4, 1.0))

# --- SUPPLEMENT SCIENCE ---
st.divider()
st.header("🧬 The Pro-Athlete Supplement Protocol")
cols = st.columns(3)
cols[0].write("**Performance:** Creatine Monohydrate (5g daily) for ATP synthesis.")
cols[1].write("**Recovery:** ZMA (Zinc, Magnesium, B6) at night for deeper sleep.")
cols[2].write("**Health:** Vitamin D3 (60k IU weekly) - common deficiency in India.")

st.caption("Developed for High Performance. Consult a physician before starting any protocol.")
