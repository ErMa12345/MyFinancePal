from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the MongoDB URI from the environment variables
mongodb_uri = os.getenv("MONGODB_URI")
# Connect to the MongoDB server
client = MongoClient(mongodb_uri)  # Update with your MongoDB connection string

# Access the database
db = client.myfinancedata  # Replace 'myfinancedata' with your database name

# Access the collection (similar to a table in relational databases)
collection = db.users  # Replace 'users' with your collection name

# Define the data to be inserted


def insert_document(data):
    # Insert one document into the collection
    try:
        result = collection.insert_one(data)
        print("Document inserted successfully with id:", result.inserted_id)
    except Exception as e:
        print("Error:", e)

def find_document(query):
    # Find a document based on a specific query
    try:
        document = collection.find_one(query)
        if document:
            return document
        else:
            return -1
    except Exception as e:
        print("Error:", e)
        return -1

def update_document(query, new_data):
    # Update the found document
    try:
        result = collection.update_one(query, {"$set": new_data})
        print("Document updated successfully:", result.modified_count, "document(s) modified.")
    except Exception as e:
        print("Error:", e)

# Example usage
# Insert a document
if __name__ == "__main__":
    insert_document({"login": "user:pass", "data" : {
            "TSLA" : 40,
            "AAPL" : 30
        }})

    # Find a document
    found_document = find_document({"login": "user:pass"})
    if found_document != -1:
        print("Found document:", found_document)
    else:
        print("Document not found.")

    # Update a document
    update_document({"login": "user:pass"}, {"data": "updated data"})