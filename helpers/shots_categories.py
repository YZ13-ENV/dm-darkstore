from firebase import db
from firebase_admin import firestore

async def getCategory(category: str):
    refTo: firestore.firestore.AsyncDocumentReference = db.collection('dm').document('bum').collection('categories').document(category)
    tags = await refTo.get()
    return tags.get('tags')