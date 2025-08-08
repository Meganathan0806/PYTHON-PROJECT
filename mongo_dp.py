from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where())
db = client["fabtech_store"]
users_collection = db["users"]

# Sample users (already hashed)
def create_sample_users():
    users = [
        {
            "name": "Meganathan B",
            "email": "meganathan@example.com",
            "username": "meganathan",
            "password": bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt()),
            "registered_at": datetime.utcnow()
        },
        {
            "name": "Priya",
            "email": "priya@example.com",
            "username": "priya25",
            "password": bcrypt.hashpw("hello123".encode("utf-8"), bcrypt.gensalt()),
            "registered_at": datetime.utcnow()
        }
    ]

    users_collection.delete_many({})  # Optional: clear old records
    users_collection.insert_many(users)
    print("Sample users inserted.")

if __name__ == "__main__":
    create_sample_users()
