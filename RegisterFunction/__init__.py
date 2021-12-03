import azure.functions as func
import json

from pymongo.collection import ReturnDocument
from ..shared.defaults import DEFAULT_HEADERS
from ..shared.session import createSession
from ..shared.user import checkUser, createUser

def main(req: func.HttpRequest) -> func.HttpResponse:
    if (req.method == "OPTIONS"):
        return func.HttpResponse(None, headers=DEFAULT_HEADERS)
    
    name = lastName = email = None
    insertedUser = session = None
    try:
        req_body = req.get_json()
        email = req_body.get('email')
        name = req_body.get('name')
        lastName = req_body.get('lastName')
        
        if checkUser(email):
            return func.HttpResponse("User exists!", status_code=400, headers=DEFAULT_HEADERS) 
        
        insertedUser = createUser(req_body) 
        session = createSession(email)
    except AttributeError:
        pass
        
    sessionData = { 
        'sessionId': session, 
        'user': {
            'name': name,
            'lastName': lastName,
            'email': email,
            'clientId': str(insertedUser.inserted_id)
        }
    }
    resp = json.dumps(sessionData)
    return func.HttpResponse(resp, headers=DEFAULT_HEADERS)