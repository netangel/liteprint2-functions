import azure.functions as func
import logging
import os
import time
import json

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
        sessionData = { 
            'session': session, 
            'name': "John Doe",
            'email': user['email']
        }
        resp = json.dumps(sessionData)
        return func.HttpResponse(resp, headers=DEFAULT_HEADERS)
    
def checkOrCreateUser(email, password, reqType, dbClient) -> ReturnDocument:
    if (email == "" or password == ""):
        raise AttributeError("Email or password is missing from the request")
    
    clientData = { 'email': email }
    
    usersTbl = dbClient.test.users
    user = usersTbl.find_one(clientData)
    
    if (user and reqType == NEW_CLIENT_REQ):
        raise AttributeError(f"Client with email {email} already exists!")
    
    if (reqType == NEW_CLIENT_REQ):
        user = usersTbl.insert_one(clientData)    
   
    if (user and password != user['password']):
        raise AttributeError(f"Incorrect password for email {email}")
    
    return user
    

def createSession(user, dbClient) -> str:
    if user == None:
        raise AttributeError("User not found!")
    else:
        sessionsTbl = dbClient.test.sessions
        userSessionObj = sessionsTbl.find_one({'user': user['email']})
        
        sessionId = None
        if (userSessionObj):
            sessionId = userSessionObj['_id']
        else:
            newSessionObj = sessionsTbl.insert_one({ 'user': user['email'], 'timestamp': time.time() })
            sessionId = newSessionObj.inserted_id
            
        return str(sessionId)