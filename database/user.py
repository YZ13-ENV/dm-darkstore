from typing import List, Optional
from firebase import db, auth


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
    if user.exists:
        userDict = user.to_dict()
        if not userDict.get('follows'):
            return False
        else: 
            follows = userDict.get('follows')
            if followId in follows:
                return True
            else:
                return False
    else:
        return False
        
async def setPlusSubscription(userId: str, subscriptionStatus: bool):
    try:
        if userId:
            auth.set_custom_user_claims(userId, { 'isSubscriber': subscriptionStatus })
        return True
    except:
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
    follows: List[str] = [followId]
    if user.exists:
        userDict = user.to_dict()
        if not userDict.get('follows'):
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
    else:
        field_updates = {
            'follows': follows
        }
        await userRef.create(document_data=field_updates)

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
        if not record.custom_claims or not record.custom_claims.get('isSubscriber'):
            auth.set_custom_user_claims(userId, { 'isSubscriber': False })
        short = {
            'short': {
                'email': record._data.get('email'),
                'displayName': record._data.get('displayName'),
                'photoUrl': record._data.get('photoUrl'),
                'isSubscriber': record.custom_claims.get('isSubscriber')
            }
        }
        return short
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
