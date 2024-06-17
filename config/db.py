from pymongo import MongoClient

def get_database():
    # Connect to the database
    client = MongoClient("mongodb://localhost:27017/")
    return client['planets_db']