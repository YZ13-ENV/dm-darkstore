from firebase import db, auth
from schemas import UserShortData

async def getShortData(userId: str):
    userRef = db.collection('users').document(userId)
    userSnap = await userRef.get()
    userDict = userSnap.to_dict()
    if (not userDict or not 'short' in userDict):
        return None
    return userDict['short']

def isShortsDataNotEq(short1: UserShortData, short2: UserShortData):
    return short1 == short2

async def getShortDataFromDB(userId: str):
    user = auth.get_user(userId)
    return user

async def setShortDataFromDB(userId: str):
    record = await getShortDataFromDB(userId=userId)
    if record:
        short = {
            'short': {
                'email': record._data['email'],
                'displayName': record._data['displayName'],
                'photoUrl': record._data['photoUrl'],
            }
        }
        userRef = db.collection('users').document(userId)
        await userRef.update(short)
        return True
    return False



async def isLocalAndDBShortEq(userId: str):
    shortData = await getShortData(userId)
    record = await getShortDataFromDB(userId=userId)
    if (record and shortData):
        shortFromRecord = {
            'email': record._data['email'],
            'displayName': record._data['displayName'],
            'photoUrl': record._data['photoUrl'],
        }
        isEq = isShortsDataNotEq(shortFromRecord, shortData)
        return isEq
    else:
        return False
    
async def checkShortData(userId: str):
    isEq = await isLocalAndDBShortEq(userId)
    if not isEq:
        await setShortDataFromDB(userId)

async def getUsersIdList():
    usersRef = db.collection('users')
    users = await usersRef.get()
    idsList = []
    for user in users:
        userId: str = user.id
        idsList.append(userId)
    return idsList

async def getUserShotWithDocId(userId: str, shotId: str):
    shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
    shotSnap = await shotRef.get()
    if (shotSnap.exists):
        shotData = shotSnap.to_dict()
        shotData['doc_id'] = shotSnap.id
        return shotData
    return None

async def getUserShotsWithDocId(userId: str, noDraft: bool=False):
    shotsRef = db.collection('users').document(userId).collection('shots')
    shots = await shotsRef.get()
    shotsList = []
    for shot in shots:
            shotData = shot.to_dict()
            shotData['doc_id'] = shot.id
            if (noDraft):
                if shotData['isDraft'] == False:
                    shotsList.append(shotData)
            else:
                shotData = shot.to_dict()
                shotData['doc_id'] = shot.id
                shotsList.append(shotData)

    return shotsList

async def getUserDrafts(userId: str):
    shotsRef = db.collection('users').document(userId).collection('shots')
    shots = await shotsRef.get()
    shotsList = []
    for shot in shots:
            shotData = shot.to_dict()
            shotData['doc_id'] = shot.id
            if shotData['isDraft'] == True:
                shotsList.append(shotData)

    return shotsList

async def getUserShots(userId: str):
    shotsRef = db.collection('users').document(userId).collection('shots')
    shots = await shotsRef.get()
    shotsList = []
    for shot in shots:
        shotData = shot.to_dict()
        shotsList.append(shotData)
    return shotsList