import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("firebase_key.json")  # Ensure the correct path
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_project_to_firebase(project_name, labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration, predicted_cost, risk_level):
    """Save project details to Firebase Firestore with correct data types."""
    
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
