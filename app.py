import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import sys  # Add this

# Ensure the "scripts/" folder is recognized as a module
sys.path.append("scripts")

# Import project scripts after fixing module path
from risk_analysis import analyze_risk
from report_generator import generate_pdf_report, generate_excel_report
from firebase_manager import save_project_to_firebase, get_all_projects

# Ensure "reports" directory exists
os.makedirs("reports", exist_ok=True)

# Load trained XGBoost model and scaler
model = joblib.load("models/xgboost_cost_estimator.pkl")
scaler = joblib.load("models/scaler.pkl")

st.title("📊 Project Cost Estimator with AI Prediction, Risk Analysis & Cloud Storage")

# User Inputs
st.sidebar.header("Enter Project Details")
project_name = st.sidebar.text_input("Project Name", value="My Project")
labor_cost = st.sidebar.number_input("Labor Cost (₹)", min_value=0, value=5000)
material_cost = st.sidebar.number_input("Material Cost (₹)", min_value=0, value=8000)
equipment_cost = st.sidebar.number_input("Equipment Cost (₹)", min_value=0, value=3000)
miscellaneous_cost = st.sidebar.number_input("Miscellaneous Costs (₹)", min_value=0, value=1000)
duration = st.sidebar.number_input("Project Duration (months)", min_value=1, value=6)

# Predict Cost
if st.sidebar.button("Predict Cost"):
    # Convert input to DataFrame with proper feature names
    input_features_df = pd.DataFrame(
        [[labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration]],
        columns=["Labor Cost", "Material Cost", "Equipment Cost", "Miscellaneous Cost", "Duration"]
    )

    # Apply feature scaling
    input_features_scaled = scaler.transform(input_features_df)

    # Predict using XGBoost model
    predicted_cost = model.predict(input_features_scaled)[0]

    st.subheader(f"🔮 Predicted Total Cost: **₹{predicted_cost:.2f}**")

    # Risk Analysis
    risk_level, risk_score = analyze_risk(labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration)
    st.subheader(f"⚠️ Risk Analysis Result: {risk_level}")
    st.progress(risk_score / 10)

    # Save to Firebase
    if save_project_to_firebase(project_name, labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration, predicted_cost, risk_level):
        st.success("✅ Project saved to Firebase successfully!")

    # Generate Reports
    pdf_file = generate_pdf_report(project_name, labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration, predicted_cost, risk_level)
    excel_file = generate_excel_report(project_name, labor_cost, material_cost, equipment_cost, miscellaneous_cost, duration, predicted_cost, risk_level)

    # Download Buttons
    if os.path.exists(pdf_file):
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name=f"{project_name}_cost_report.pdf",
                mime="application/pdf"
            )

    if os.path.exists(excel_file):
        with open(excel_file, "rb") as f:
            st.download_button(
                label="📊 Download Excel Report",
                data=f,
                file_name=f"{project_name}_cost_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Display Saved Projects
st.sidebar.subheader("📂 Saved Projects")
if st.sidebar.button("Load Saved Projects"):
    projects = get_all_projects()
    if projects:
        for project in projects:
            st.write(f"📌 **{project['Project Name']}** | Cost: ₹{project['Predicted Total Cost (₹)']:.2f} | Risk: {project['Risk Level']}")
    else:
        st.warning("No projects saved yet.")
