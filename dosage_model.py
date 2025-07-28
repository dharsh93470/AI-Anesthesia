import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the dataset
df = pd.read_csv("sample_patient_dosage_dataset.csv")

# Drop PatientID (non-numeric)
df = df.drop(columns=["PatientID"])

# Encode categorical columns
df['Gender'] = pd.factorize(df['Gender'])[0]
df['SurgeryType'] = pd.factorize(df['SurgeryType'])[0]
df['ASA_Class'] = pd.factorize(df['ASA_Class'])[0]
df['ValveHealth'] = pd.factorize(df['ValveHealth'])[0]
df['HeartHealth'] = pd.factorize(df['HeartHealth'])[0]
df['ECGPattern'] = pd.factorize(df['ECGPattern'])[0]

# Split features and targets
X = df.drop(columns=["Propofol_mg", "Fentanyl_mcg", "Atracurium_mg"])
y = df[["Propofol_mg", "Fentanyl_mcg", "Atracurium_mg"]]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "anesthesia_dosage_model.pkl")

# Evaluate
print("Model training complete. Test R^2 score:", model.score(X_test, y_test))
