import os
import io
import re
import requests
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.runtime.scriptrunner import RerunException, RerunData
import numpy as np
import time
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import joblib
import calendar
from datetime import datetime
import streamlit as st
import streamlit as st
from chatbot import chatbot_page








# Load the model once at the top of the script (so it loads only once per session)
model = joblib.load("anesthesia_dosage_model.pkl")


st.set_page_config(page_title="Live Vitals", layout="wide")

CSV_FILE = os.path.join(os.path.dirname(__file__), "patients.csv")

users = {
    "doctor": "password123",
    
}

def load_patients():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE).to_dict(orient="records")
    return []

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "patients" not in st.session_state:
    st.session_state.patients = load_patients()
if "view_patient" not in st.session_state:
    st.session_state.view_patient = None
if "live_patient" not in st.session_state:
    st.session_state.live_patient = None


def rerun():
    raise RerunException(RerunData())

def save_patients(patients):
    pd.DataFrame(patients).to_csv(CSV_FILE, index=False)

def load_patients():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE).to_dict(orient="records")
    return []

def login_page():
    st.title(" 💉AI Anesthesia Assistant ")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if users.get(username) == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome Dr. {username}!")
            rerun()
        else:
            st.error("Invalid username or password")

def sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/ios-filled/100/ffffff/hospital-room.png", width=60)
        st.markdown("<h2 style='color:white;'>AI Assistant</h2>", unsafe_allow_html=True)
        return option_menu(
            menu_title=None,
            options=["Home", "Account", "Chat", "Patients", "Live Vitals","Feedback"],
            icons=["house", "person", "chat", "calendar4-week", "activity", "Pen"],
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "5px", "background-color": "#002B5B"},
                "icon": {"color": "white", "font-size": "18px"},
                "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "5px"},
                "nav-link-selected": {"background-color": "#005f73", "font-weight": "bold"},
            },
        )

def calculate_dosage(weight, surgery_type):
    base_dose = 2
    surgery_factor = {
        "Appendectomy": 1.0,
        "Cholecystectomy": 1.2,
        "Cesarean Section": 1.5,
        "Hernia Repair": 1.1,
        "Orthopedic Surgery": 1.3,
        "ENT Surgery": 1.0,
        "Cardiac Bypass": 2.0,
    }
    factor = surgery_factor.get(surgery_type, 1)
    dosage = weight * base_dose * factor
    return round(dosage, 2)

def generate_dynamic_ecg_wave(heart_rate, duration=10):
    t = np.linspace(0, duration, duration * 100)
    bpm = heart_rate
    beat_period = 60 / bpm
    ecg = np.sin(2 * np.pi * t / beat_period) * np.exp(-2 * (t % beat_period))
    ecg += 0.1 * np.random.normal(size=len(t))  # add small noise
    return t, ecg



def fetch_vitals_from_api(device_id):
    try:
        response = requests.get(f"http://your-api-server/api/v1/vitals/{device_id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "HeartRate": data.get("heart_rate"),
                "BloodPressure": data.get("blood_pressure"),
                "ValveHealth": data.get("valve_health"),
                "HeartHealth": data.get("heart_health")
            }
    except Exception as e:
        st.warning(f"Could not fetch vitals: {e}")
    return None



import streamlit as st
import calendar
from datetime import datetime
import pandas as pd

def dashboard():
    st.markdown(f"<h1 style='color:white;'>Doctor Dashboard – Dr. {st.session_state.username}</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Total Patients Card
    with col1:
        st.markdown("""
        <div style='background-color:#1e1e2f;padding:20px;border-radius:10px;'>
            <h4 style='color:#8ecdf6;'>Total Patients</h4>
            <h2 style='color:white;'>200+</h2>
            <p style='color:#999;'>Till Today</p>
        </div>
        """, unsafe_allow_html=True)

    # Today Patients Card
    with col2:
        st.markdown("""
        <div style='background-color:#1e1e2f;padding:20px;border-radius:10px;'>
            <h4 style='color:#8ecdf6;'>Today Patients</h4>
            <h2 style='color:white;'>068</h2>
            <p style='color:#999;'>17 May 2025</p>
        </div>
        """, unsafe_allow_html=True)

    # Today Appointments Card
    with col3:
        st.markdown("""
        <div style='background-color:#1e1e2f;padding:20px;border-radius:10px;'>
            <h4 style='color:#8ecdf6;'>Today Appointments</h4>
            <h2 style='color:white;'>085</h2>
            <p style='color:#999;'>17 May 2025</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    calendar_table()  # Show calendar below the cards

def generate_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    df = pd.DataFrame(cal, columns=days)
    return df

def calendar_table():
    st.markdown("<h2 style='color:white;'>Monthly Calendar</h2>", unsafe_allow_html=True)
    today = datetime.today()
    year, month = today.year, today.month
    df = generate_calendar(year, month)
    st.dataframe(df, width=370, height=210)



    

   

# ========= PATIENT DASHBOARD WITH EDITABLE FIELDS =========
def patient_dashboard(patient):
    st.markdown(f"<h2 style='color:#00d4ff;'>Patient Dashboard – {patient['Name']}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3011/3011270.png", width=150)
        st.markdown(f"""
        - **Name:** {patient['Name']}  
        - **Age:** {patient['Age']}  
        - **Sex:** {patient['Gender']}  
        - **Surgery:** {patient['Surgery']}  
        - **Weight:** {patient.get('Weight', 'N/A')} kg  
        - **Device ID:** {patient.get('DeviceID', 'None')}  
        """)

    with col2:
        st.markdown("### \U0001FA80 Health Metrics")
        st.metric("Heart's Health", f"{patient.get('HeartHealth', '90%')}")
        st.metric("Valve's Health", f"{patient.get('ValveHealth', '80%')}")
        st.metric("Blood Pressure", f"{patient.get('BloodPressure', '110/70 mmHg')}")
        st.metric("Heart Rate", f"{patient.get('HeartRate', '85 bpm')}")

        try:
            weight = float(patient.get("Weight", 0))
            if weight > 0 and patient["Surgery"]:
                dose = calculate_dosage(weight, patient["Surgery"])
                st.metric("Anesthesia Dosage (mg)", dose)
        except Exception:
            pass

        if patient.get("DeviceID"):
            if st.button("🔄 Fetch Real-Time Vitals from Monitor"):
                vitals = fetch_vitals_from_api(patient["DeviceID"])
                if vitals:
                    patient.update(vitals)
                    save_patients(st.session_state.patients)
                    st.success("Vitals updated from monitor!")
                    rerun()
                else:
                    st.error("Failed to retrieve data from device.")

    # 👉 Medical History Section
    st.markdown("### 🩺 Medical History")
    history = patient.get("MedicalHistory", "")
    if history:
        if isinstance(history, list):
            for item in history:
                st.markdown(f"- {item}")
        else:
            st.markdown(history)
    else:
        st.info("No medical history available.")

    # 👉 Medication Section
    st.markdown("### 💊 Current Medication")
    meds = patient.get("Medication", "")
    if meds:
        if isinstance(meds, list):
            for med in meds:
                st.markdown(f"- {med}")
        else:
            st.markdown(meds)
    else:
        st.info("No medications recorded.")

        # ✅ Edit Form - stays inside st.form
    with st.expander("✏️ Edit Patient Details"):
        with st.form(f"edit_form_{patient['Name']}"):
            name = st.text_input("Name", value=patient["Name"])
            age = st.number_input("Age", min_value=0, max_value=120, value=int(patient["Age"]))
            gender = st.selectbox("Gender", ["Male", "Female", "Other"],
                                  index=["Male", "Female", "Other"].index(patient["Gender"]))
            surgery_list = [
                "Appendectomy", "Cholecystectomy", "Cesarean Section",
                "Hernia Repair", "Orthopedic Surgery", "ENT Surgery", "Cardiac Bypass"
            ]
            try:
                surgery_index = surgery_list.index(patient["Surgery"])
            except ValueError:
                surgery_index = 0
            surgery = st.selectbox("Surgery", surgery_list, index=surgery_index)
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=float(patient["Weight"]))
            device_id = st.text_input("Device ID", value=patient.get("DeviceID", ""))
            med_history = st.text_area("Medical History", value=patient.get("MedicalHistory", ""))
            medication = st.text_area("Medication", value=patient.get("Medication", ""))

            submitted = st.form_submit_button("💾 Save Changes")
            if submitted:
                patient.update({
                    "Name": name,
                    "Age": age,
                    "Gender": gender,
                    "Surgery": surgery,
                    "Weight": weight,
                    "DeviceID": device_id,
                    "MedicalHistory": med_history,
                    "Medication": medication
                })
                save_patients(st.session_state.patients)
                st.success("Patient details updated!")
                rerun()

    # ✅ DELETE BUTTON - outside the form
    st.markdown("---")
    delete_col, back_col = st.columns([1, 2])
    if delete_col.button("🗑️ Delete Patient"):
        st.session_state.confirm_delete = True

    if st.session_state.get("confirm_delete"):
        st.warning("Are you sure you want to delete this patient? This action cannot be undone.")
        if st.button("✅ Confirm Delete"):
            st.session_state.patients = [
                p for p in st.session_state.patients
                if not (p["Name"] == patient["Name"] and p["Age"] == patient["Age"] and p["Gender"] == patient["Gender"])
            ]
            save_patients(st.session_state.patients)
            st.session_state.view_patient = None
            st.session_state.confirm_delete = False
            st.success("Patient deleted successfully!")
            rerun()

    # 🔙 Back button
    if back_col.button("🔙 Back to Patients"):
        st.session_state.view_patient = None
        st.session_state.confirm_delete = False
        rerun()






def appointments_page():
    if st.session_state.view_patient:
        patient_dashboard(st.session_state.view_patient)
        return

    st.subheader("📋 Existing Patients")
    if st.session_state.patients:
        for i, patient in enumerate(st.session_state.patients):
            cols = st.columns([4, 1])
            cols[0].markdown(f"**{patient['Name']}**, {patient['Age']}y, {patient['Gender']}, {patient['Surgery']}")
            if cols[1].button("🔍 View", key=f"view_{i}"):
                st.session_state.view_patient = patient
                rerun()
    else:
        st.info("No patients yet. Add a new one below.")

    st.markdown("---")
    st.subheader("➕ Add New Patient")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    surgery = st.selectbox("Surgery Type", [
        "Appendectomy", "Cholecystectomy", "Cesarean Section",
        "Hernia Repair", "Orthopedic Surgery", "ENT Surgery", "Cardiac Bypass"
    ])
    weight = st.number_input("Weight (kg)", min_value=1, max_value=300, step=1)

    device_id = st.text_input("Device ID (optional)")
    medical_history = st.text_area("Medical History (e.g., Diabetes, Hypertension)", height=100)
    medication = st.text_area("Current Medication (e.g., Metformin, Atenolol)", height=100)

    if st.button("Add Patient"):
        if not name:
            st.error("Please enter patient name.")
        else:
            new_patient = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Surgery": surgery,
                "Weight": weight,
                "DeviceID": device_id,
                "MedicalHistory": medical_history,
                "Medication": medication
            }
            st.session_state.patients.append(new_patient)
            save_patients(st.session_state.patients)
            st.success("Patient added successfully!")
            rerun()

    st.markdown("---")
    st.subheader("📁 Upload Patient CSV")

    uploaded_file = st.file_uploader("Upload CSV file with patient data", type=["csv"])
    if uploaded_file:
        import pandas as pd

        try:
            df = pd.read_csv(uploaded_file)

            required_columns = {"Name", "Age", "Gender", "Surgery", "Weight"}
            if not required_columns.issubset(df.columns):
                st.error(f"CSV must contain the following columns: {', '.join(required_columns)}")
            else:
                existing_patient_keys = {
                    (p["Name"], p["Age"], p["Gender"]) for p in st.session_state.patients
                }

                for _, row in df.iterrows():
                    key = (row["Name"], int(row["Age"]), row["Gender"])
                    if key in existing_patient_keys:
                        continue  # Skip if already exists

                    patient = {
                        "Name": row["Name"],
                        "Age": int(row["Age"]),
                        "Gender": row["Gender"],
                        "Surgery": row["Surgery"],
                        "Weight": float(row["Weight"]),
                        "DeviceID": row.get("DeviceID", ""),
                        "MedicalHistory": row.get("MedicalHistory", ""),
                        "Medication": row.get("Medication", "")
                    }
                    st.session_state.patients.append(patient)
                    existing_patient_keys.add(key)

                save_patients(st.session_state.patients)
                st.success("CSV data uploaded and patients added successfully!")
                rerun()
        except Exception as e:
            st.error(f"Failed to read CSV file: {e}")



def generate_ecg_graph(heart_rate):
    fs = 500  # Sampling frequency (Hz)
    duration = 2  # seconds
    t = np.linspace(0, duration, fs * duration)
    f = heart_rate / 60  # frequency in Hz

    ecg = 0.1 * np.sin(2 * np.pi * f * t)
    for beat_time in np.arange(0, duration, 1/f):
        idx = (np.abs(t - beat_time)).argmin()
        if idx + 2 < len(ecg):
            ecg[idx] += 1
            ecg[idx+1] -= 0.5
            ecg[idx+2] += 0.2
    return t, ecg

import streamlit as st
import numpy as np
import time
import matplotlib.pyplot as plt
import plotly.graph_objs as go

def generate_ecg_wave(heart_rate, duration=2, fs=500):
    t = np.linspace(0, duration, int(fs * duration))
    bpm = heart_rate / 60
    ecg = np.sin(2 * np.pi * bpm * t) * np.exp(-3 * t % 1)
    noise = 0.05 * np.random.randn(len(t))
    return t, ecg + noise



def safe_int(val, default=0):
    try:
        return int(val)
    except:
        return default

def safe_float(val, default=0.0):
    try:
        return float(val)
    except:
        return default

def generate_ecg_wave(hr):
    t = np.linspace(0, 1, 250)
    ecg = 0.6 * np.sin(2 * np.pi * hr / 60 * t * 5) + 0.4 * np.sin(2 * np.pi * hr / 60 * t * 15)
    return t, ecg

def live_vitals_page():
    st.subheader("🩺 Live Vitals Monitoring")

    if not st.session_state.get("patients"):
        st.info("No patients available. Please add patients first.")
        return

    patient_names = [p["Name"] for p in st.session_state.patients]
    selected_name = st.selectbox("Select Patient", patient_names)

    patient = next((p for p in st.session_state.patients if p["Name"] == selected_name), None)
    if not patient:
        st.error("Selected patient not found.")
        return

    st.markdown(f"### Current Vitals for {patient['Name']}")
    col1, col2 = st.columns([2, 3])

    def safe_int_spo2(val, default=98):
        try:
            if val is None:
                return default
            return int(str(val).replace('%', '').strip())
        except (ValueError, TypeError):
            return default

    def safe_int(val, default):
        try:
            if val is None:
                return default
            return int(val)
        except (ValueError, TypeError):
            return default

    def safe_float(val, default):
        try:
            if val is None:
                return default
            return float(val)
        except (ValueError, TypeError):
            return default

    with col1:
        st.markdown("### Enter/Update Vitals Manually")

        heart_rate = st.number_input(
            "Heart Rate (bpm)", 
            min_value=30, max_value=200, 
            value=safe_int(patient.get("HeartRate"), 85)
        )
        blood_pressure = st.text_input(
            "Blood Pressure (e.g., 120/80 mmHg)", 
            value=patient.get("BloodPressure", "110/70 mmHg")
        )
        spo2 = st.slider(
            "Oxygen Saturation (SpO₂ %)",
            70, 100,
            safe_int_spo2(patient.get("SpO2"), 98)
        )
        respiratory_rate = st.number_input(
            "Respiratory Rate (breaths/min)", 
            min_value=5, max_value=40, 
            value=safe_int(patient.get("RespiratoryRate"), 16)
        )
        etco2 = st.slider(
            "End-Tidal CO₂ (mmHg)", 
            20, 60, 
            safe_int(patient.get("ETCO2"), 35)
        )
        temperature = st.number_input(
            "Temperature (°C)", 
            min_value=30.0, max_value=42.0, 
            value=safe_float(patient.get("Temperature"), 36.5), 
            step=0.1
        )

        operation_type = st.selectbox(
            "Select Surgery Type",
            ["Cardiac Surgery", "Neurosurgery", "Abdominal Surgery",
             "Emergency Trauma", "Orthopedic Surgery", "Dental Surgery",
             "Eye Surgery", "Plastic Surgery","Ceserean", "Other"],
            key="surgery_type_for_analysis"
        )
       
    


        if st.button("🧪 Analyze Vitals and Recommend Dosage"):
            # Save vitals to patient data and session state
            patient["HeartRate"] = heart_rate
            patient["BloodPressure"] = blood_pressure
            patient["SpO2"] = spo2
            patient["RespiratoryRate"] = respiratory_rate
            patient["ETCO2"] = etco2
            patient["Temperature"] = temperature
            save_patients(st.session_state.patients)  # Your existing save function

            st.session_state["last_analysis"] = {
                "patient": patient,
                "vitals": {
                    "HeartRate": heart_rate,
                    "BloodPressure": blood_pressure,
                    "SpO2": spo2,
                    "RespiratoryRate": respiratory_rate,
                    "ETCO2": etco2,
                    "Temperature": temperature
                },
                "operation_type": operation_type
            }

    with col2:
        st.markdown("### 🔄 Live ECG & Vital Summary")
        live_mode = st.checkbox("▶️ Enable Live Vitals Animation", value=False)
        vitals_placeholder = st.empty()
        ecg_graph_placeholder = st.empty()

        def display_vitals(hr, spo2_val, rr, co2, temp):
            with vitals_placeholder.container():
                st.metric("Heart Rate", f"{hr} bpm")
                st.metric("Blood Pressure", blood_pressure)
                st.metric("Oxygen Saturation", f"{spo2_val} %")
                st.metric("Respiratory Rate", f"{rr} breaths/min")
                st.metric("End-Tidal CO₂", f"{co2} mmHg")
                st.metric("Temperature", f"{temp} °C")

        if live_mode:
            for _ in range(30):
                heart_rate = max(30, min(200, heart_rate + np.random.randint(-2, 3)))
                spo2 = max(70, min(100, spo2 + np.random.choice([-1, 0, 1])))
                respiratory_rate = max(5, min(40, respiratory_rate + np.random.choice([-1, 0, 1])))
                etco2 = max(20, min(60, etco2 + np.random.choice([-1, 0, 1])))
                temperature = max(30.0, min(42.0, round(temperature + np.random.choice([-0.1, 0, 0.1]), 1)))

                display_vitals(heart_rate, spo2, respiratory_rate, etco2, temperature)

                t, ecg = generate_ecg_wave(heart_rate)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=t, y=ecg, mode='lines', line=dict(color='cyan', width=2)))
                fig.update_layout(
                    title=f"Simulated ECG - HR: {heart_rate} bpm",
                    paper_bgcolor='rgb(10,10,30)',
                    plot_bgcolor='rgb(10,10,30)',
                    font=dict(color='white'),
                    xaxis=dict(showgrid=False, showticklabels=False),
                    yaxis=dict(showgrid=False, showticklabels=False),
                    height=250,
                    margin=dict(t=20, b=20, l=20, r=20),
                )
                ecg_graph_placeholder.plotly_chart(fig, use_container_width=True)
                time.sleep(1.5)
        else:
            display_vitals(heart_rate, spo2, respiratory_rate, etco2, temperature)
            t, ecg = generate_ecg_wave(heart_rate)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=ecg, mode='lines', line=dict(color='cyan', width=2)))
            fig.update_layout(
                title=f"Simulated ECG - HR: {heart_rate} bpm",
                paper_bgcolor='rgb(10,10,30)',
                plot_bgcolor='rgb(10,10,30)',
                font=dict(color='white'),
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=False, showticklabels=False),
                height=250,
                margin=dict(t=20, b=20, l=20, r=20),
            )
            ecg_graph_placeholder.plotly_chart(fig, use_container_width=True)

    if "last_analysis" in st.session_state:
        st.markdown("---")
        st.subheader("🤖 AI Suggested Dosage Plan")

        analysis = st.session_state["last_analysis"]
        patient = analysis["patient"]
        vitals = analysis["vitals"]
        operation_type = analysis["operation_type"]

        base_dose = 2.0  # mg/kg for Propofol induction

        hr_factor = 1 + (vitals["HeartRate"] - 75) / 100
        temp_factor = 1 + (vitals["Temperature"] - 36.5) / 10
        spo2_factor = 1 if vitals["SpO2"] >= 95 else 0.8
        rr_factor = 1 if vitals["RespiratoryRate"] >= 12 else 0.85

        try:
            bp_systolic = int(vitals["BloodPressure"].split('/')[0])
        except Exception:
            bp_systolic = 110
        bp_factor = 1 if bp_systolic >= 90 else 0.75

        final_dose = base_dose * hr_factor * temp_factor * spo2_factor * rr_factor * bp_factor
        final_dose = round(final_dose, 2)

        fentanyl_dose = round(1.5 * hr_factor * spo2_factor * rr_factor, 2)

        if vitals["SpO2"] < 92 or vitals["RespiratoryRate"] < 10:
            rocuronium_dose = 0.6
        else:
            rocuronium_dose = 0.9

        st.markdown(f"### Patient: **{patient['Name']}** | Surgery Type: **{operation_type}**")
        st.write(f"**Heart Rate:** {vitals['HeartRate']} bpm")
        st.write(f"**Blood Pressure:** {vitals['BloodPressure']}")
        st.write(f"**SpO₂:** {vitals['SpO2']}%")
        st.write(f"**Respiratory Rate:** {vitals['RespiratoryRate']} breaths/min")
        st.write(f"**ETCO₂:** {vitals['ETCO2']} mmHg")
        st.write(f"**Temperature:** {vitals['Temperature']} °C")

        if operation_type in ["Cardiac Surgery", "Neurosurgery"]:
            st.markdown(f"**Recommendation**: General Anesthesia")
            st.write(f"💉 Propofol (Induction): **{final_dose} mg/kg**")
            st.write(f"💉 Fentanyl (Opioid): **{fentanyl_dose} mcg/kg**")
            st.write(f"💉 Rocuronium (Muscle Relaxant): **{rocuronium_dose} mg/kg**")
            st.write(f"💊 Optional Antiemetic: Ondansetron 4 mg IV")
        elif operation_type == "Orthopedic Surgery":
            st.markdown(f"**Recommendation**: Regional Anesthesia")
            st.write("💉 Bupivacaine: 0.25% - 0.5%, 15-20 ml")
        else:
            st.markdown(f"**Recommendation**: Balanced Anesthesia")
            st.write(f"💉 Propofol: **{final_dose} mg/kg**")
            st.write(f"💉 Fentanyl: **{fentanyl_dose} mcg/kg**")
            st.write(f"💉 Rocuronium: **{rocuronium_dose} mg/kg**")
            st.write(f"💊 Optional Antiemetic: Ondansetron 4 mg IV")

        st.info("These values are estimated. Always verify with clinical judgement.")
            # ⚠️ Vital Sign Cautions
        st.markdown("### ⚠️ Vital Sign Cautions")
        cautions = []
        if bp_systolic < 90:
            cautions.append("Low Blood Pressure (Systolic < 90 mmHg)")
        if vitals["HeartRate"] < 60:
            cautions.append("Low Heart Rate (Bradycardia)")
        if vitals["SpO2"] < 92:
            cautions.append("Low Oxygen Saturation (SpO₂ < 92%)")
        if vitals["RespiratoryRate"] < 10:
            cautions.append("Low Respiratory Rate (< 10 breaths/min)")

        if cautions:
            for caution in cautions:
                st.warning(caution)
        else:
            st.success("✅ All vitals are within normal range.")

        # 🧠 AI Summary of Dosage Logic
        st.markdown("### 🧠 AI Decision Summary")
        summary_parts = []
        if bp_systolic < 90:
            summary_parts.append("low blood pressure")
        if vitals["SpO2"] < 92:
            summary_parts.append("reduced oxygen saturation")
        if vitals["RespiratoryRate"] < 10:
            summary_parts.append("slow respiratory rate")
        if vitals["HeartRate"] < 60:
            summary_parts.append("low heart rate")

        if summary_parts:
            explanation = "💡 Dosage was adjusted due to " + ", ".join(summary_parts) + " to ensure safe anesthesia delivery."
        else:
            explanation = "💡 Vitals were stable, allowing standard dosage with minor adjustments based on heart rate and temperature."

        st.info(explanation)

                # 🩹 Pain Relief and Post-Surgery Measures
        st.markdown("### 🩹 Pain Management & Post-Surgery Measures")

        if operation_type in ["Cardiac Surgery", "Neurosurgery", "Orthopedic Surgery"]:
            st.write("**Post-op Pain Relief:**")
            st.write("- IV Paracetamol 1g every 6 hours")
            st.write("- IV Ketorolac 30mg every 8 hours (if renal function normal)")
            st.write("- Consider PCA (Patient-Controlled Analgesia) with Morphine for high pain procedures")

            st.write("**Monitoring & Measures:**")
            st.write("- Continuous ECG & SpO₂ monitoring for 24h")
            st.write("- Hourly vitals for first 6h post-op")
            st.write("- Early mobilization within 24h if stable")

        elif operation_type in ["Dental Surgery", "Eye Surgery", "Plastic Surgery"]:
            st.write("**Post-op Pain Relief:**")
            st.write("- Oral Ibuprofen 400mg every 8 hours")
            st.write("- Paracetamol 500-1000mg every 6 hours")
            st.write("- Ice pack application for 10–15 minutes if swelling occurs")

            st.write("**Monitoring & Measures:**")
            st.write("- Monitor for nausea or vomiting")
            st.write("- Discharge instructions for oral hygiene and wound care")
        
        else:
            st.write("**Post-op Pain Relief:**")
            st.write("- IV Paracetamol 1g every 6h OR oral as tolerated")
            st.write("- IV Tramadol 50-100mg if moderate pain persists")

            st.write("**Monitoring & Measures:**")
            st.write("- Regular pain score assessments (VAS scale)")
            st.write("- Early ambulation and incentive spirometry")
            st.write("- Wound care and infection monitoring")

        st.info("🧾 Pain management and post-op care are generalized. Tailor based on patient-specific factors and surgical protocols.")


import streamlit as st
import json
from datetime import datetime

FEEDBACK_FILE = "doctor_feedback.json"

def load_feedback():
    try:
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_feedback(feedback_list):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(feedback_list, f, indent=2)

def doctor_feedback_page():
    st.title("🩺 Doctor Feedback on AI Anesthesia Assistant")
    st.markdown("""
    Please help us improve the tool by providing your valuable feedback.  
    Rate different aspects and leave detailed comments or suggestions.
    """)

    with st.form("feedback_form"):
        overall_rating = st.slider("Overall Performance Rating", 1, 5, 4, help="Rate overall satisfaction")
        usability = st.slider("Usability", 1, 5, 4)
        accuracy = st.slider("Accuracy of Recommendations", 1, 5, 4)
        speed = st.slider("Speed of Response", 1, 5, 4)
        helpfulness = st.slider("Helpfulness of Guidance", 1, 5, 4)

        comments = st.text_area("Detailed Feedback / Suggestions", height=150)

        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            feedback_list = load_feedback()
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "overall_rating": overall_rating,
                "usability": usability,
                "accuracy": accuracy,
                "speed": speed,
                "helpfulness": helpfulness,
                "comments": comments
            }
            feedback_list.append(feedback_entry)
            save_feedback(feedback_list)
            st.success("Thank you for your feedback! Your input will help improve the assistant.")

    # Optional: Show previous feedback (aggregated or raw)
    if st.checkbox("Show recent feedback from doctors"):
        feedback_list = load_feedback()
        if feedback_list:
            st.markdown(f"### Last {min(5, len(feedback_list))} Feedback Entries:")
            for fb in feedback_list[-5:][::-1]:
                st.markdown(f"**Date:** {fb['timestamp']}")
                st.markdown(f"- Overall: {fb['overall_rating']} ⭐")
                st.markdown(f"- Usability: {fb['usability']} ⭐")
                st.markdown(f"- Accuracy: {fb['accuracy']} ⭐")
                st.markdown(f"- Speed: {fb['speed']} ⭐")
                st.markdown(f"- Helpfulness: {fb['helpfulness']} ⭐")
                if fb['comments']:
                    st.markdown(f"- Comments: {fb['comments']}")
                st.markdown("---")
        else:
            st.info("No feedback yet. Be the first to submit!")






def account_page():
    st.subheader("User Account")
    st.write(f"Logged in as: {st.session_state.username}")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        rerun()


def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False  # or your default login state

    if not st.session_state.logged_in:
        login_page()
        return

    # Initialize page if not set
    if "page" not in st.session_state:
        st.session_state.page = "Home"

    choice = sidebar()

    # Update session state page according to sidebar choice
    st.session_state.page = choice

    if choice == "Home":
        dashboard()
    elif choice == "Account":
        account_page()
    if choice == "Chat":
        chatbot_page()
    elif choice == "Patients":
        appointments_page()
    elif choice == "Live Vitals":
        live_vitals_page()
    elif choice == "Feedback":
        doctor_feedback_page()
    else:
        st.info("This section is under development.")


if __name__ == "__main__":
    main()
