from typing import List, Optional
from firebase import db, auth
# from schemas.user import UserShortData
from helpers import isShortsDataNotEq


def getUsersIdList():
    authUsers = auth.list_users().users
    idsList = []

    for user in authUsers:
        userId: str = user.uid
        idsList.append(userId)
        
    return idsList

async def isInFollowList(userId: str, followId: str):
    userRef = db.collection('users').document(userId)
    user = await userRef.get()
    userDict = user.to_dict()
    if not userDict.get('follows'):
        return False
    else: 
        follows = userDict.get('follows')
        if followId in follows:
            return True
        else:
            return False
        
async def getFollows(userId: str):
    userRef = db.collection('users').document(userId)
    user = await userRef.get()
    userDict = user.to_dict()
    if not userDict.get('follows'):
        return []
    else: 
        return userDict.get('follows')
    
async def stopFollow(userId: str, followId: str):
    userRef = db.collection('users').document(userId)
    user = await userRef.get()
    userDict = user.to_dict()
    if not userDict.get('follows'):
        return True
    else:
        follows: List[str] = userDict.get('follows')
        filteredFollows = list(filter(lambda uid: uid != followId, follows))
        field_updates = {
            'follows': filteredFollows
        }
        await userRef.update(field_updates=field_updates)
        return True

async def startFollow(userId: str, followId: str):
    userRef = db.collection('users').document(userId)
    user = await userRef.get()
    userDict = user.to_dict()
    if not userDict.get('follows'):
        follows: List[str] = [followId]
        field_updates = {
            'follows': follows
        }
        await userRef.update(field_updates=field_updates)
        return True
    else:
        follows: List[str] = userDict.get('follows')
        follows.append(followId)
        field_updates = {
            'follows': follows
        }
        await userRef.update(field_updates=field_updates)
        return True

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
                'email': record._data.get('email'),
                'displayName': record._data.get('displayName'),
                'photoUrl': record._data.get('photoUrl'),
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
                'email': record._data.get('email'),
                'displayName': record._data.get('displayName'),
                'photoUrl': record._data.get('photoUrl'),
            }
        }
        return short
    else:
        return None

async def getShortDataByEmail(email: str):
    try:
        record = auth.get_user_by_email(email=email)
        if record:
            short = {
                'short': {
                    'email': record._data.get('email'),
                    'displayName': record._data.get('displayName'),
                    'photoUrl': record._data.get('photoUrl'),
                }
            }
            return short
    except:
        return None

async def getUserUIDByEmail(email: str):
    try:
        record = auth.get_user_by_email(email=email)
        if record:
            return record._data.get('uid')
    except:
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
            'email': record._data.get('email'),
            'displayName': record._data.get('displayName'),
            'photoUrl': record._data.get('photoUrl'),
        }
        isEq = isShortsDataNotEq(shortFromRecord, shortData)
        return isEq
    else:
        return False
    
async def checkShortData(userId: str):
    isEq = await isLocalAndDBShortEq(userId)
    if not isEq:
        await setShortDataFromDB(userId)