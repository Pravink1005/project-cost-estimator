import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# 🔥 Debug: Print Firebase secrets to check structure
st.write("🔥 Firebase Secrets Debug:", st.secrets["firebase"])

# Convert Streamlit secrets into a valid dictionary
firebase_secrets = dict(st.secrets["firebase"])

# Ensure private_key formatting (Fixes \n issues)
firebase_secrets["private_key"] = firebase_secrets["private_key"].replace("\\n", "\n")

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_secrets)
    firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

def save_project_to_firebase(project_name, labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration, predicted_cost, risk_level):
    """Save project details to Firebase Firestore."""
    project_data = {
        "Project Name": str(project_name),
        "Labor Cost (₹)": float(labor_cost),
        "Material Cost (₹)": float(material_cost),
        "Equipment Cost (₹)": float(equipment_cost),
        "Miscellaneous Cost (₹)": float(miscellaneous_cost),
        "Duration (months)": int(duration),
        "Predicted Total Cost (₹)": float(predicted_cost),
        "Risk Level": str(risk_level)
    }
    db.collection("projects").document(project_name).set(project_data)
    return True

def get_all_projects():
    """Retrieve all saved projects from Firebase."""
    projects = db.collection("projects").stream()
    return [{**doc.to_dict(), "id": doc.id} for doc in projects]
