from typing import Optional
from firebase import db, auth
# from schemas.user import UserShortData
from helpers import isShortsDataNotEq
async def getUsersIdList():
    usersRef = db.collection('users')
    users = await usersRef.get()
    idsList = []

    for user in users:
        userId: str = user.id
        idsList.append(userId)

    return idsList


async def updateUser(userId: str, displayName: Optional[str], photoUrl: Optional[str]):
    if (displayName and not photoUrl):
        auth.update_user(uid=userId, displayName=displayName)
        return True
    if (not displayName and photoUrl):
        auth.update_user(uid=userId, photoUrl=photoUrl)
        return True
    if (displayName and photoUrl):
        auth.update_user(uid=userId, displayName=displayName, photoUrl=photoUrl)
        return True

    return False

async def getShortData(userId: str):
    userRef = db.collection('users').document(userId)
    userSnap = await userRef.get()
    userDict = userSnap.to_dict()
    if (not userDict or not 'short' in userDict):
        return None
    return userDict['short']


async def setShortDataFromDB(userId: str):
    record = await getUserRecord(userId=userId)
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

async def getShortDataFromRecord(userId: str):
    record = await getUserRecord(userId=userId)
    if record:
        short = {
            'short': {
                'email': record._data['email'],
                'displayName': record._data['displayName'],
                'photoUrl': record._data['photoUrl'],
            }
        }
        return short
    else:
        return None


async def getUserRecord(userId: str):
    try:
        user = auth.get_user(userId)
        return user
    except:
        return None

async def isLocalAndDBShortEq(userId: str):
    shortData = await getShortData(userId)
    record = await getUserRecord(userId=userId)
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