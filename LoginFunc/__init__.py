import logging
import azure.functions as func
import json

from ..shared.defaults import *
from ..shared.user import checkUserWithPassword
from ..shared.session import createSession

def main(req: func.HttpRequest) -> func.HttpResponse:
    if (req.method == "OPTIONS"):
        return func.HttpResponse(None, headers=DEFAULT_HEADERS)

    email = password = None
    try:
        req_body = req.get_json()
        email = req_body.get('email')
        password = req_body.get('password')
    except ValueError:
        logging.error(f"Wrong request: {str(req)}")
    
    user = session = resp = None
    resp_code = 400
    try:
        user = checkUserWithPassword(email, password)
        session = createSession(user)
    except AttributeError as err:
        resp = str(err)
    else:
        sessionData = { 
            'sessionId': session, 
            'user': {
                'email'     : user['email'],
                # 'name'      : user['name'],
                # 'lastName'  : user['lastName'] 
            }
        }
        resp = json.dumps(sessionData)
        resp_code = 200
    
    return func.HttpResponse(resp, status_code=resp_code, headers=DEFAULT_HEADERS)
