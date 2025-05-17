from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

uri = "mongodb+srv://hardikkumar885:Admin123@cluster0.lzlx07f.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
except ServerSelectionTimeoutError as e:
    print(f"Server selection timeout: {e}")
except Exception as e:
    print(f"An error occurred: {e}")