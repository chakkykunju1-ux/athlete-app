import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, time

# --- APP CONFIG ---
st.set_page_config(page_title="APEX ALPHA: PRO PROTOCOL", page_icon="🔱", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff; }
    .circadian-card { background: #111; padding: 15px; border-radius: 10px; border-left: 5px solid #ffaa00; margin-bottom: 10px; }
    .meal-card { background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; }
    .time-stamp { color: #ffaa00; font-weight: bold; font-family: 'Courier New'; }
    .exercise-box { background: #000; padding: 15px; border: 1px solid #00ffcc; border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CALCULATIONS ---
def get_alpha_metrics(w, h, a, g, act, goal_wt, deadline):
    bmr = (10*w) + (6.25*h) - (5*a) + (5 if g=="Male" else -161)
    tdee = bmr * act
    days_rem = max((deadline - date.today()).days, 1)
    target_cal = tdee - ((w - goal_wt) * 7700 / days_rem)
    
    # Precise Gram-Scale Macro Calculation
    prot = w * 2.6 # High protein for muscle sparing
    fats = w * 0.8 # Essential fats for hormones
    carbs = (target_cal - (prot*4) - (fats*9)) / 4
    return round(target_cal), round(prot), round(carbs), round(fats), bmr

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔱 ATHLETE BIO-DATA")
    curr_w = st.number_input("Weight (kg)", 40.0, 150.0, 85.0)
    goal_w = st.number_input("Goal Weight (kg)", 40.0, 150.0, 75.0)
    deadline = st.date_input("Deadline Date", date(2026, 4, 1))
    wake_time = st.time_input("Wake Time", time(5, 0))
    h = st.number_input("Height (cm)", 140, 210, 180)
    a = st.number_input("Age", 18, 60, 25)
    g = st.radio("Gender", ["Male", "Female"])
    intensity = st.select_slider("Load", options=[1.2, 1.375, 1.55, 1.725, 1.9], value=1.725)

cal, p, c, f, bmr = get_alpha_metrics(curr_w, h, a, g, intensity, goal_w, deadline)

# --- DASHBOARD ---
st.title("🔱 APEX ALPHA COMMAND CENTER")
st.markdown(f"**PROTOCOL:** {round((curr_w-goal_w)/((deadline-date.today()).days/7), 2)}kg/week Loss")

m1, m2, m3, m4 = st.columns(4)
m1.metric("FUEL (KCAL)", f"{cal}")
m2.metric("PROTEIN (G)", f"{p}")
m3.metric("CARBS (G)", f"{c}")
m4.metric("FATS (G)", f"{f}")

t1, t2, t3, t4 = st.tabs(["🕒 CIRCADIAN SCHEDULE", "🏋️ 7-DAY BATTLE PLAN", "🍱 NUTRITION SCALE", "🔋 ELITE RECOVERY"])

with t1:
    st.subheader("Hourly Biological Optimization")
    def hr(t, h): return (datetime.combine(date.today(), t) + pd.Timedelta(hours=h)).time().strftime('%H:%M')
    
    st.markdown(f"""
    <div class='circadian-card'><span class='time-stamp'>{hr(wake_time, 0)}</span>: <b>Hydration & Light:</b> 500ml Water + Pink Salt. 10 mins sunlight for circadian Reset.</div>
    <div class='circadian-card'><span class='time-stamp'>{hr(wake_time, 1.5)}</span>: <b>First Macro Load:</b> High protein + high fat. First Caffeine dose.</div>
    <div class='circadian-card' style='border-left-color: #00ffcc;'><span class='time-stamp'>{hr(wake_time, 10)}</span>: <b>PEAK PERFORMANCE:</b> Body temp max. Train Now (60 min High Intensity).</div>
    <div class='circadian-card' style='border-left-color: #ff4b4b;'><span class='time-stamp'>{hr(wake_time, 14)}</span>: <b>Blue Light Block:</b> Melatonin prep. No screens or calories.</div>
    """, unsafe_allow_html=True)
    

with t2:
    st.subheader("6-Day High-Volume Split (1 Hour)")
    day = st.selectbox("Select Training Day", ["Day 1: Chest & Shoulders (Push)", "Day 2: Back & Rear Delts (Pull)", "Day 3: Quads & Calves", "Day 4: Arms & Forearms", "Day 5: Hamstrings & Lower Back", "Day 6: Full Body Explosive", "Day 7: Active Recovery"])
    
    st.markdown("#### 1. WARM-UP (10 MIN)")
    st.write("Dynamic Stretching: Arm Circles, Leg Swings, Cat-Cow, Band Pull-aparts.")
    
    st.markdown("#### 2. MAIN WORKOUT (40 MIN)")
    if "Day 1" in day:
        st.write("Bench Press 4x8 | Incline DB Press 3x12 | Military Press 3x10 | Lateral Raises 4x15 | Dips 3xAMRAP")
        st.image("https://www.strengthlog.com/wp-content/uploads/2020/03/bench-press.gif", width=400)
    elif "Day 2" in day:
        st.write("Deadlifts 3x5 | Weighted Pull-ups 4x8 | Barbell Rows 4x10 | Face Pulls 4x20 | DB Curls 3x12")
        st.image("https://www.strengthlog.com/wp-content/uploads/2020/03/Deadlift.gif", width=400)
    elif "Day 3" in day:
        st.write("Back Squat 4x8 | Leg Press 3x15 | Leg Extensions 4x20 | Standing Calf Raises 5x15")
        st.image("https://www.strengthlog.com/wp-content/uploads/2020/03/Squat.gif", width=400)
    
    st.markdown("#### 3. COOL-DOWN (10 MIN)")
    st.write("Static Stretching: Focus on worked muscles. 5 mins Box Breathing (4s In, 4s Hold, 4s Out, 4s Hold).")
    

with t3:
    st.subheader("Gram-Specific Nutrition Scale")
    st.write(f"Based on your 2.6g Protein/kg target. Use a digital kitchen scale for these measurements.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='meal-card'>
            <b>Breakfast:</b> 200g Egg Whites + 2 Whole Eggs + 60g Oats (Dry weight)
        </div>
        <div class='meal-card'>
            <b>Lunch:</b> 200g Chicken Breast (Raw weight) + 150g Cooked Basmati + 100g Broccoli
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='meal-card'>
            <b>Pre-Workout:</b> 1 Apple + 1 Scoop Whey in Water
        </div>
        <div class='meal-card'>
            <b>Dinner:</b> 200g White Fish + 150g Sweet Potato + Large Salad
        </div>
        """, unsafe_allow_html=True)
    

with t4:
    st.subheader("Elite Recovery Protocol")
    r1, r2 = st.columns(2)
    with r1:
        st.write("**Daily Supplement Stack:**")
        st.info("Creatine 5g | Citrulline 8g | Omega-3 3000mg | Magnesium Bisglycinate 400mg")
    with r2:
        st.write("**Recovery Tactics:**")
        st.error("Cold Plunge (11°C): 3 mins (Reduces Inflammation)")
        st.success("Sauna (80°C): 20 mins (Heat Shock Proteins)")
    

st.divider()
st.caption("APEX ALPHA V6.0 | GLOBAL ATHLETE STANDARDS")
