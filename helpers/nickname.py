from firebase import db
from firebase_admin import firestore

async def getUidByNickName(nickname: str):
    nicknameRef: firestore.firestore.AsyncDocumentReference = db.collection('dm').document('users').collection('nicknames').document(nickname)
    docSnap = await nicknameRef.get()
    if (docSnap.exists):
        docDict = docSnap.to_dict()
        uid = docDict.get('uid')
        return uid
    else: return None