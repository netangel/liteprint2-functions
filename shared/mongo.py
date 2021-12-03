from os import environ
from pymongo import MongoClient
from pymongo.database import Database
from .defaults import DB_NAME

def getClient() -> MongoClient:
    appMode = environ['AZURE_FUNCTIONS_ENVIRONMENT'] 
    if appMode == 'Development':
        url = environ['MONGO_DB_URL']
    else:
        url = None

    return MongoClient(url)

def getDb(dbName = DB_NAME) -> Database: 
    client = getClient()
    return client.get_database(dbName)