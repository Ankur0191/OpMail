# storage/firestore_client.py
from google.cloud import firestore
import os

_project = os.getenv("FIRESTORE_PROJECT_ID")

def get_client():
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set to the path of the service account JSON
    if _project:
        return firestore.Client(project=_project)
    else:
        return firestore.Client()
