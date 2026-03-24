# namespace std
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="Mindset Check-in", page_icon="🌱", layout="centered")

# 2. Visual Styling
st.html("""
    <style>
    .main { background-color: #f7f9fc; }
    .stButton > button { background-color: #5d8aa8; color: white; border-radius: 20px; border: none; padding: 10px 20px; }
    .stTextArea textarea { border-radius: 10px; }
    </style>
    """)

st.title("🌱 The Inner Landscape")
st.write("A space for you to reflect before we begin our journey together.")

# --- SECTION 1: IDENTITY ---
name = st.text_input("What should we call you? (You can use a nickname)", placeholder="e.g., Star-Gazer")

# --- SECTION 2: THE VISUAL TASKS ---
st.divider()
st.subheader("Task 1: Mood Weather")
mood = st.select_slider(
    "If your current mental state was a sky, what would it look like?",
    options=["⛈️ Stormy", "☁️ Overcast", "🌤️ Partly Cloudy", "☀️ Clear Blue", "🌈 Vibrant"]
)

st.subheader("Task 2: Battery Check")
energy = st.slider("Drag the slider to show your current social battery (0-100%):", 0, 100, 50)

# --- SECTION 3: PSYCHOLOGICAL NEEDS & CHOICES ---
st.divider()
st.subheader("Task 3: Deep Roots (Psychological Needs)")
st.write("Which of these do you feel is currently 'thirstiest' in your life?")
psych_need = st.radio(
    "Choose the one that resonates most:",
    [
        "🎨 Autonomy: I need more freedom to be myself.", 
        "🏆 Competence: I need to feel like I'm capable of handling my tasks.", 
        "🤝 Relatedness: I need a deeper connection with others."
    ]
)

st.subheader("Task 4: The Path Forward")
st.write("If you encountered a fork in the road today, which path would you naturally take?")
choice_path = st.selectbox(
    "Pick your instinctive path:",
    [
        "The Quiet Path: Focusing on rest and internal peace.",
        "The Brave Path: Facing a challenge head-on even if it's scary.",
        "The Social Path: Seeking strength through talking and community.",
        "The Curious Path: Trying something completely new and unknown."
    ]
)

# --- SECTION 4: TALK FROM HEART ---
st.divider()
st.subheader("🤍 Talk from the Heart")
st.write("This part is totally anonymous. Share one thing that is weighing on your heart, or a message you wish someone would tell you right now.")
heart_msg = st.text_area("Your anonymous message...", placeholder="Type whatever you're feeling. No judgment here.")

# --- SUBMISSION LOGIC ---
# namespace std

# --- SUBMISSION LOGIC ---
if st.button("Submit My Journey Entry"):
    if not name or not heart_msg:
        st.error("Please provide a name/nickname and share a small message from the heart!")
    else:
        try:
            # 1. Connect to Google Sheets
            conn = st.connection("gsheets", type=GSheetsConnection)
            
            # 2. Hard-link the URL from secrets
            sheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
            
            # 3. Read existing data
            existing_data = conn.read(spreadsheet=sheet_url)
            
            # 4. Format the new row
            new_row = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Name": name,
                "Mood": mood,
                "Energy": f"{energy}%",
                "Focus_Areas": "Psych-Focused Entry", 
                "Psych_Need": psych_need,
                "Choice_Path": choice_path,
                "Heart_Message": heart_msg
            }])
            
            # 5. Append and Update
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(spreadsheet=sheet_url, data=updated_df)
            
            st.balloons()
            st.success("Your heart-felt response has been safely recorded. See you at the workshop!")
            
        except Exception as e:
            st.error("Connection Error. Please verify your Google Sheet URL is correct in the Streamlit Secrets.")
            st.write(e)
