import pandas as pd
import numpy as np

np.random.seed(42)

n = 200  # Number of patients

data = {
    "PatientID": [f"P{str(i).zfill(4)}" for i in range(1, n+1)],
    "Age": np.random.randint(18, 90, size=n),
    "Gender": np.random.choice(["Male", "Female"], size=n),
    "Weight_kg": np.round(np.random.uniform(50, 120, size=n), 1),
    "Height_cm": np.round(np.random.uniform(140, 200, size=n), 1),
    "SurgeryType": np.random.choice(["Cardiac", "Orthopedic", "Neuro", "General"], size=n),
    "ASA_Class": np.random.choice(["I", "II", "III", "IV"], size=n),
    "HeartRate_bpm": np.random.randint(50, 121, size=n),
    "BP_Systolic": np.random.randint(90, 181, size=n),
    "BP_Diastolic": np.random.randint(60, 111, size=n),
    "SpO2_%": np.random.randint(90, 101, size=n),
    "ValveHealth": np.random.choice(["Normal", "Mild", "Moderate", "Severe"], size=n),
    "HeartHealth": np.random.choice(["Normal", "Mild", "Moderate", "Severe"], size=n),
    "ECGPattern": np.random.choice(["Normal", "Abnormal"], size=n),
    "Propofol_mg": np.round(np.random.uniform(50, 300, size=n), 1),
    "Fentanyl_mcg": np.round(np.random.uniform(50, 300, size=n), 1),
    "Atracurium_mg": np.round(np.random.uniform(10, 100, size=n), 1),
}

df = pd.DataFrame(data)
df.to_csv("sample_patient_dosage_dataset.csv", index=False)
print("Synthetic dataset saved as sample_patient_dosage_dataset.csv")
