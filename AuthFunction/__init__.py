import azure.functions as func
import logging
import os
import time

from pymongo import MongoClient
from pymongo.collection import ReturnDocument

DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, access-control-allow-origin'
}

NEW_CLIENT_REQ = "newClient"

def main(req: func.HttpRequest) -> func.HttpResponse:
    if (req.method == "OPTIONS"):
        return func.HttpResponse(None, headers=DEFAULT_HEADERS)
    
    appMode = os.environ['AZURE_FUNCTIONS_ENVIRONMENT'] 
    email = password = reqType = None
    
    try:
        req_body = req.get_json()
        email = req_body.get('email')
        password = req_body.get('password')
        reqType = req_body.get('requestType')
    except ValueError:
        logging.error(f"Wrong request: {req.method}")
    
    if appMode == 'Development':
        url = os.environ['MONGO_DB_URL']
    else:
        url = None

    dbClient = MongoClient(url)

    user = session = None
    try:
        user = checkOrCreateUser(email, password, reqType, dbClient)
        session = createSession(user, dbClient)
    except AttributeError as err:
        return func.HttpResponse(str(err), status_code=400, headers=DEFAULT_HEADERS) 
    else:
        return func.HttpResponse(session, headers=DEFAULT_HEADERS)
    
def checkOrCreateUser(email, password, reqType, dbClient) -> ReturnDocument:
    if (email == "" or password == ""):
        raise AttributeError("Email or password is missing from the request")
    
    clientData = {'email': email, 'password': password}
    
    usersTbl = dbClient.test.users
    user = usersTbl.find_one(clientData)
    
    print(user)
    
    if (user and reqType == NEW_CLIENT_REQ):
        raise AttributeError(f"Client with email {email} already exists!")
    
    if (reqType == NEW_CLIENT_REQ):
        user = usersTbl.insert_one(clientData)    
    
    return user
    

def createSession(user, dbClient) -> str:
    if user == None:
        raise AttributeError("User not found!")
    else:
        sessionsTbl = dbClient.test.sessions
        userSessionObj = sessionsTbl.find_one({'user': user['email']})
        
        if (not userSessionObj):
            newSessionObj = sessionsTbl.insert_one({ 'user': user['email'], 'timestamp': time.time() })
            return str(newSessionObj.inserted_id)
            
        return str(userSessionObj['_id'])