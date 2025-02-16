import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Retrieve Firebase credentials from Streamlit Secrets
firebase_secrets = dict(st.secrets["firebase"])

# Ensure private_key has correct newlines
firebase_secrets["private_key"] = firebase_secrets["private_key"].replace("\\n", "\n")

# Debugging: Print Firebase Secrets to verify correctness
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
