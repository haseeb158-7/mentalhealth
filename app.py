import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page Styling
st.set_page_config(page_title="Mindset Check-in", page_icon="🧘", layout="centered")

# Custom CSS for a calming look
st.markdown("""
    <style>
    .main { background-color: #f0f4f8; }
    div.stButton > button:first-child { background-color: #4a7c59; color: white; }
    </style>
  """, unsafe_allow_html=True)

st.title("🌱 Pre-Workshop Mindset Check-in")
st.write("Before we begin our 4-day journey, let's map out our collective energy.")

# --- THE VISUAL TASKS ---

# Task 1: Narrative Intro
name = st.text_input("First, what should we call you?")

# Task 2: The Mood Weather (Visual Choice)
st.subheader("Task 1: The Weather Inside")
mood = st.select_slider(
    "If your current mental state was a sky, what would it look like?",
    options=["⛈️ Stormy", "☁️ Overcast", "🌤️ Partly Cloudy", "☀️ Clear Blue", "🌈 Vibrant"]
)

# Task 3: The Battery Check (Visual Slider)
st.subheader("Task 2: Power Levels")
energy = st.slider("How much 'social battery' do you have left for today?", 0, 100, 50)
if energy < 20:
    st.caption("⚠️ Looks like you're running on empty. We'll keep things low-pressure!")

# Task 4: Priority Mapping
st.subheader("Task 3: The Focus Compass")
focus = st.multiselect(
    "Which areas are currently 'heavy' in your mind?",
    ["Academic Pressure", "Sleep Quality", "Social Anxiety", "Future Planning", "Self-Care Habits"],
    max_selections=3
)

# --- SUBMISSION LOGIC ---

if st.button("Submit My Entry"):
    if not name or not focus:
        st.error("Please provide your name and pick at least one focus area!")
    else:
        # Connect to GSheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Prepare the new row
        new_row = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Name": name,
            "Mood": mood,
            "Energy": f"{energy}%",
            "Focus_Areas": ", ".join(focus)
        }])
        
        # Update sheet (Appends to existing data)
        existing_data = conn.read()
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(data=updated_df)
        
        st.balloons()
        st.success(f"Thank you, {name}! Your response has been recorded.")
