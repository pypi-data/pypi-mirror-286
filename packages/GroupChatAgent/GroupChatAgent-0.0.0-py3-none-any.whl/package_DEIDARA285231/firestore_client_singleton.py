from firebase_admin import firestore

class FirestoreClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirestoreClientSingleton, cls).__new__(cls)
            cls._instance.client = firestore.Client()
        return cls._instance