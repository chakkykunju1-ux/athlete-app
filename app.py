import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, time

# --- APP CONFIG ---
st.set_page_config(page_title="APEX PRO: ELITE COMMAND", page_icon="🔱", layout="wide")

# --- CUSTOM CSS FOR PREMIUM DARK AESTHETIC ---
st.markdown("""
    <style>
    .stApp { background: #050505; color: #ffffff; }
    .metric-card { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #00ffcc; text-align: center; }
    .exercise-card { background: #1a1a1a; padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 5px solid #00ffcc; }
    .circadian-box { background: #111; padding: 15px; border-radius: 10px; border-left: 5px solid #ffaa00; margin-bottom: 10px; }
    .time-label { color: #ffaa00; font-weight: bold; font-family: 'Courier New'; }
    .supp-card { background: #0d1b2a; padding: 15px; border-radius: 10px; border: 1px solid #1b263b; margin-bottom: 10px; }
    .sci-header { color: #00ffcc; font-family: 'Monospace'; font-weight: bold; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# --- ADVANCED MATH ENGINE ---
def calculate_pro_metrics(w, h, a, g, act, goal_wt, target_date):
    bmr = (10*w) + (6.25*h) - (5*a) + (5 if g=="Male" else -161)
    tdee = bmr * act
    
    # Deadline Math
    days_remaining = (target_date - date.today()).days
    weeks_remaining = max(days_remaining / 7, 1)
    total_kg_to_lose = w - goal_wt
    
    # 7700 cals = 1kg fat
    daily_deficit = (total_kg_to_lose * 7700) / max(days_remaining, 1)
    target_cal = tdee - daily_deficit
    
    # Pro Athlete Macros: High Protein (2.5g/kg) for muscle sparing
    prot = w * 2.5 
    fats = (target_cal * 0.20) / 9
    carbs = (target_cal - (prot*4) - (fats*9)) / 4
    
    return round(target_cal), round(prot), round(carbs), round(fats), round(weeks_remaining), round(total_kg_to_lose/weeks_remaining, 2), round(bmr)

# --- SIDEBAR: COACHING COMMAND ---
with st.sidebar:
    st.title("🎖️ STRATEGY HUB")
    name = st.text_input("Athlete Name", "CHAMP")
    
    st.markdown("### 📅 MISSION TIMELINE")
    curr_w = st.number_input("Current Weight (kg)", 40.0, 160.0, 85.0)
    goal_w = st.number_input("Goal Weight (kg)", 40.0, 160.0, 75.0)
    deadline = st.date_input("Deadline Date", date(2026, 6, 1))
    
    st.markdown("### 🧬 BIOMETRICS")
    h = st.number_input("Height (cm)", 140, 220, 180)
    a = st.number_input("Age", 18, 65, 25)
    g = st.radio("Gender", ["Male", "Female"])
    intensity = st.select_slider("Activity Level", options=[1.2, 1.375, 1.55, 1.725, 1.9], value=1.725)
    
    st.divider()
    wake_time = st.time_input("Typical Wake Up Time", time(6, 0))

# Run Calculations
cal, p, c, f, wks, rate, bmr_val = calculate_pro_metrics(curr_w, h, a, g, intensity, goal_w, deadline)

# --- MAIN DASHBOARD ---
st.title(f"🚀 MISSION: {goal_w}KG BY {deadline}")
st.write(f"Athlete: **{name.upper()}** | Window: **{wks} Weeks** | Required Rate: **{rate} kg/week**")

# TARGET GRID
c1, c2, c3, c4 = st.columns(4)
c1.metric("DAILY KCAL", f"{cal}")
c2.metric("PROTEIN (g)", f"{p}")
c3.metric("CARBS (g)", f"{c}")
c4.metric("FATS (g)", f"{f}")

st.divider()

# --- PROFESSIONAL TABS ---
t_circadian, t_train, t_diet, t_supp, t_recov = st.tabs([
    "🕒 CIRCADIAN TIMING", "🏋️ VISUAL TRAINING", "🍱 NUTRITION", "💊 SUPPLEMENTS", "🔋 RECOVERY"
])

with t_circadian:
    st.subheader("Biological Clock Optimization")
    st.info("Aligning nutrition and intensity with hormonal peaks.")
    
    def add_hrs(t, hrs): return (datetime.combine(date.today(), t) + pd.Timedelta(hours=hrs)).time()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='circadian-box'>
            <span class='time-label'>{wake_time.strftime('%H:%M')} - {add_hrs(wake_time, 1).strftime('%H:%M')}</span><br>
            <b>CORTISOL SPIKE:</b> View sunlight. Hydrate + Pink Salt. No caffeine for 90m.
        </div>
        <div class='circadian-box' style='border-left-color: #00ffcc;'>
            <span class='time-label'>{add_hrs(wake_time, 9).strftime('%H:%M')}</span><br>
            <b>STRENGTH PEAK:</b> Body temp is highest. Grip strength and coordination peak. <b>TRAIN NOW.</b>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='circadian-box' style='border-left-color: #0575E6;'>
            <span class='time-label'>{add_hrs(wake_time, 12).strftime('%H:%M')}</span><br>
            <b>GLYCOGEN REPLENISHMENT:</b> High-carb post-workout meal.
        </div>
        <div class='circadian-box' style='border-left-color: #ff4b4b;'>
            <span class='time-label'>{add_hrs(wake_time, 14).strftime('%H:%M')}</span><br>
            <b>MELATONIN WINDOW:</b> Blue light blockers on. Deep sleep prep for GH release.
        </div>
        """, unsafe_allow_html=True)
    
    

with t_train:
    st.subheader("Visual Movement Vault")
    day = st.selectbox("Select Training Day", ["Day 1: Heavy Push", "Day 2: Power Pull", "Day 3: Elite Legs"])
    
    if "Push" in day:
        st.markdown("<div class='exercise-card'><span class='sci-header'>Exercise 1: Barbell Bench Press</span><br>4 Sets x 6-8 Reps</div>", unsafe_allow_html=True)
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHYxcXp5YmF5Znd5bmx4bmZ5bmZ5bmZ5bmZ5bmZ5bmZ5bmZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKu5In2e07Wrg9W/giphy.gif")
        
        
        st.markdown("<div class='exercise-card'><span class='sci-header'>Exercise 2: Overhead Press</span><br>3 Sets x 10 Reps</div>", unsafe_allow_html=True)
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHYxcXp5YmF5Znd5bmx4bmZ5bmZ5bmZ5bmZ5bmZ5bmZ5bmZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/l0HlSrf8X6Z3oJm6s/giphy.gif")
    
    elif "Legs" in day:
        st.markdown("<div class='exercise-card'><span class='sci-header'>Exercise 1: Barbell Back Squat</span><br>4 Sets x 6 Reps</div>", unsafe_allow_html=True)
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOHYxcXp5YmF5Znd5bmx4bmZ5bmZ5bmZ5bmZ5bmZ5bmZ5bmZ5JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKu5In2e07Wrg9W/giphy.gif")
        

with t_diet:
    st.subheader("Elite Indian Performance Diet")
    st.info(f"Targeting {rate}kg/week. Focus on High TEF (Thermal Effect of Food).")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.error("🥩 NON-VEG ELITE")
        st.write("- **Breakfast:** 6 Egg Whites + 1 Whole Egg + Oats")
        st.write("- **Lunch:** 200g Chicken + 1 cup Rice + Dal + Salad")
        st.write("- **Dinner:** 200g Fish + Stir-fry Veggies + Lemon Water")
    with col_d2:
        st.success("🥦 VEG ELITE")
        st.write("- **Breakfast:** 150g Paneer + 2 Jowar Rotis + Curd")
        st.write("- **Lunch:** 100g Soya Chunks + Dal + Brown Rice")
        st.write("- **Dinner:** Moong Dal Chilla + Tofu Stir-fry + Sprouts")
    

with t_supp:
    st.subheader("Bio-Availability Timing")
    st.table(pd.DataFrame({
        "Supplement": ["Creatine", "Caffeine", "Whey Protein", "Magnesium/ZMA", "Vitamin D3"],
        "Best Time": ["Post-Workout (with carbs)", "30 min Pre-Workout", "Post-Workout", "Before Bed", "With Breakfast"],
        "Pro Benefit": ["ATP Recovery", "CNS Drive", "Muscle Repair", "Recovery", "Hormones"]
    }))

with t_recov:
    st.subheader("Bio-Feedback Tracker")
    hrv = st.slider("Heart Rate Variability (HRV)", 20, 100, 70)
    sleep_hrs = st.slider("Sleep Duration", 4, 12, 8)
    if sleep_hrs < 7:
        st.warning("⚠️ High CNS Fatigue Risk. Consider a deload session.")
    

st.divider()
st.caption("APEX PRO V5.0 | 2026 WORLD CLASS PERFORMANCE | CIRCADIAN & DEADLINE ENGINE")
