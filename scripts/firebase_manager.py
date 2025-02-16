import firebase_admin
from firebase_admin import credentials, firestore
import json
import os

# Load Firebase credentials from JSON file
with open("firebase_key.json") as f:
    firebase_secrets = json.load(f)

# Initialize Firebase only if it hasn't been initialized before
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(firebase_secrets)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase Initialized Successfully!")
    except ValueError as e:
        print(f"❌ Firebase Initialization Failed: {str(e)}")
        exit(1)

# Connect to Firestore
db = firestore.client()
