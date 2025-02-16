import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

# Convert Streamlit secrets into a proper JSON dictionary
firebase_secrets = json.loads(json.dumps(st.secrets["firebase"]))

# Fix private_key formatting
firebase_secrets["private_key"] = firebase_secrets["private_key"].replace("\\n", "\n")

# Debugging: Print Firebase secrets to verify correctness
st.write("✅ Firebase Secrets Debug:", firebase_secrets)

# Initialize Firebase only if it hasn't been initialized before
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_secrets)
        firebase_admin.initialize_app(cred)
        st.success("✅ Firebase Initialized Successfully!")
    except ValueError as e:
        st.error(f"❌ Firebase Initialization Failed: {str(e)}")
        st.stop()

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
