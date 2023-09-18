import datetime
from typing import Iterable
from firebase import db
from firebase_admin.firestore import firestore

async def add_in_history(userId: str, historyQuery: str):
    historyColl: firestore.CollectionReference = db.collection('users').document(userId).collection('history').document('search').collection('dey')
    res = []
    similarQueries: Iterable[firestore.DocumentSnapshot] = await historyColl.where('query', '==', historyQuery.lower()).get()
    for qr in similarQueries:
        qr_dict = qr.to_dict()
        qr_dict.update({ 'queryId': qr.id })
        res.append(qr_dict)
    if (len(res) == 0):
        try :
            query = {
                'query': historyQuery,
                'createdAt': datetime.datetime.now().timestamp()
            }
            await historyColl.add(document_data=query)
            return True
        except:
            return False
    else:
        for qr in res:
            qrRef: firestore.DocumentReference = historyColl.document(qr['queryId'])
            qrDoc: firestore.DocumentSnapshot = await historyColl.document(qr['queryId']).get()
            qr_dict = qrDoc.to_dict()
            qr_dict.update({ 'createdAt': datetime.datetime.now().timestamp() })
            await qrRef.update(field_updates=qr_dict)
