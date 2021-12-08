from pymongo.collection import ReturnDocument
from pymongo.results import InsertOneResult

from .mongo import MyMongo 

def checkUserWithPassword(email, password) -> ReturnDocument:
    if (email == "" or password == ""):
        raise AttributeError("Email or password is missing from the request")
   
    userRecord = checkUser(email)
    
    if (userRecord and userRecord['password'] == password):
        return userRecord
   
    raise AttributeError("User not found") 
    
def checkUser(email) -> ReturnDocument:
    if (email == None or email == ""):
        raise AttributeError("Email is missing from the request")
    
    clientData = { 'email': email }
    return MyMongo().getDb().users.find_one(clientData)

def createUser(userDara) -> InsertOneResult:
    # More checks?
    return MyMongo().getDb().users.insert_one(userDara)