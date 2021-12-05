from os import environ
from pymongo import MongoClient
from pymongo.database import Database
from .defaults import DB_NAME

def getClient() -> MongoClient:
    url = environ['MONGO_DB_URL']
    return MongoClient(url)

def getDb(dbName = DB_NAME) -> Database: 
    client = getClient()
    return client.get_database(dbName)