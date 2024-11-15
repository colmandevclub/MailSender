import firebase_admin
from firebase_admin import credentials, auth, firestore
import pandas as pd

# Initialize Firebase Admin SDK
cred = credentials.Certificate("colmandevclubwebsite-firebase-key.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()


# Function to get user data from Firebase Authentication and Firestore
def fetch_user_data():
    # Get all users from Firebase Authentication
    auth_users = auth.list_users().users

    # Initialize list to store user data
    user_data = []

    # Iterate through each authenticated user
    for index, user in enumerate(auth_users):
        print(f"index: {index}")
        # Get user email from Firebase Authentication
        user_email = user.email

        # Fetch additional user data from Firestore where document ID = UID
        user_doc = db.collection("users-v2").document(user.uid).get()
        if user_doc.exists:
            user_info = user_doc.to_dict()
            applicant_data = user_info['appliciant_data']
            user_info['email'] = user_email
            user_info.update(applicant_data)
            user_data.append(user_info)
        else:
            print(f"No Firestore document found for user {user_email}")

    return user_data


# Fetch data and export to Excel
def export_to_excel():
    user_data = fetch_user_data()
    # Convert data to a DataFrame
    df = pd.DataFrame(user_data)
    # Export DataFrame to Excel
    df.to_excel("output/firebase_user_data.xlsx", index=False)
    print("Data exported to firebase_user_data.xlsx")


# Run export function
export_to_excel()
