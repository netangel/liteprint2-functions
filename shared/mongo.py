from os import environ
from pymongo import MongoClient
from pymongo.database import Database
from .defaults import DB_NAME

class MyMongo(object):

    __instance = None
    __dbCLient = None
    
    def __new__(self):
        if self.__instance is None:
            self.__instance = super(MyMongo, self).__new__(self)
            url = environ['MONGO_DB_URL']
            self.__dbCLient = MongoClient(url)

        return self.__instance
   
    def getClient(self) -> MongoClient:
        return MyMongo().__dbCLient

    def getDb(self) -> Database: 
        client = MyMongo().__dbCLient
        return client.get_database(DB_NAME)