from pymongo import MongoClient

mongoServer = "mongodb://localhost:27017/self_project2"

client = MongoClient(mongoServer)

db = client["self_project2"]

def get_collection(collection_name):
    return db[collection_name]