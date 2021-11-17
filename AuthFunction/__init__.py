import azure.functions as func
import logging
import os
import pymongo

DEFAULT_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, access-control-allow-origin'
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    if (req.method == "OPTIONS"):
        return func.HttpResponse(None, headers=DEFAULT_HEADERS)
    
    appMode = os.environ['AZURE_FUNCTIONS_ENVIRONMENT'] 
    email = None
    password = None
    
    try:
        req_body = req.get_json()
    except ValueError:
        logging.error(f"Wrong request: {req.method}")
    else:
        email = req_body.get('email')
        password = req_body.get('password')
    
    if appMode == 'Development':
        url = os.environ['MONGO_DB_URL']
    else:
        url = None

    dbClient = pymongo.MongoClient(url)

    if email and password:
        user = checkUserExists(email, password, dbClient)
        if not user:
            return func.HttpResponse(f"User with emaill {email} not found", status_code=400, headers=DEFAULT_HEADERS)
        
        session = createSession(user, dbClient)
        
        return func.HttpResponse({'sessionId': session}, headers=DEFAULT_HEADERS)
    else:
        return func.HttpResponse(
            "Email or password is missing from the request",
            status_code=400,
            headers=DEFAULT_HEADERS
        ) 

def checkUserExists(email, password, dbClient) -> pymongo.ReturnDocument:
    db = dbClient.db
    return db.users.find_one({'email': email})

def createSession(user, dbClient) -> str:
    if user == None:
        return None
    else:
        return "123abc"
        
    