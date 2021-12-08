from .mongo import MyMongo
import time

def createSession(email) -> str:
    userSessionObj = getSessionByUser(email)
    
    sessionId = None
    
    if (userSessionObj):
        sessionId = userSessionObj['_id']
    else:
        newSessionObj = MyMongo().getDb().sessions.insert_one({ 'user': email, 'timestamp': time.time() })
        sessionId = newSessionObj.inserted_id
            
    return str(sessionId)
    
def getSessionByUser(email) -> str:
    if email == None:
        raise AttributeError("Email is undefined!")
    
    return MyMongo().getDb().sessions.find_one({'user': email})
    