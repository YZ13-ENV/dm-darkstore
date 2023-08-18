import httpx
from datetime import datetime
from typing import Any, Dict, List, Optional
from database.user import getFollows, getUsersIdList
from firebase import db
from schemas.draft import DraftToPublish
from schemas.shot import ShotData, ShotDataForUpload
from host import host
def getCreatedDate(el):
    return el['createdAt']

def getViews(el):
    return len(el['views'])

async def addShotAsDraft(userId: str, shotId: str, shot: ShotDataForUpload):
    # post
    draftRef = db.collection('users').document(userId).collection('shots').document(shotId)
    draftSnap = await draftRef.get()
    dictDraft = shot.model_dump()
    filledDraft = {
        'isDraft': True,
        'authorId': userId,
        'title': dictDraft['title'],
        'rootBlock': dictDraft['rootBlock'],
        'blocks': dictDraft['blocks'],
        'createdAt': datetime.today().timestamp()
    }
    if draftSnap.exist:
        return False
    else:
        draftRef.set(filledDraft)
        return True

async def publishDraft(userId: str, draftId: str, draft: DraftToPublish):
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    draftSnap = await draftRef.get()
    dictDraft = draft.model_dump()
    filledShot = {
        **dictDraft,
        'isDraft': False,
        'authorId': userId,
        'createdAt': datetime.today().timestamp(),
        'likes': [],
        'views': [],
        'comments': [],
    }
    if (draftSnap.exists):
        filledShot.update({'createdAt': draftSnap.get('createdAt'), 'thumbnail': draftSnap.get('thumbnail')})
        if dictDraft.get('thumbnail') == None:
            filledShot.pop('thumbnail')
            await draftRef.set(filledShot)
        await draftRef.set(filledShot)
        return True
    else:
        return False

async def updateShot(userId: str, shotId: str, shot: ShotData):
    shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
    dictShot = shot.model_dump()
    if (dictShot.get('doc_id') != None):
        dictShot.pop('doc_id')
        await shotRef.update(dictShot)
        return True
    else:
        await shotRef.update(dictShot)
        return True


async def updateDraft(userId: str, draftId: str, draft: ShotDataForUpload):
    # patch
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    draftSnap = await draftRef.get()
    dictDraft = draft.model_dump()
    filledDraft = {
        **dictDraft,
        'isDraft': True,
        'authorId': userId,
        'createdAt': datetime.today().timestamp(),
    }
    if (not draftSnap.exists):
        await draftRef.set(filledDraft)
        return True
    else:
        snapDict = draftSnap.to_dict()
        filledDraft.update({'createdAt': snapDict.get('createdAt')})
        await draftRef.update(filledDraft)
        return True
    
async def addOrRemoveLike(shotAuthorId: str, shotId: str, uid: str):
    shotRef = db.collection('users').document(shotAuthorId).collection('shots').document(shotId)
    shotSnap = await shotRef.get()
    shotDict: Dict[str, Any] = shotSnap.to_dict()
    likes: List[str] = shotDict.get('likes')
    if (uid in likes):
        filteredLikes = []
        for likerUID in likes:
            if likerUID != uid:
                filteredLikes.append(likerUID)
        shotDict.update({'likes': filteredLikes})
        await shotRef.update(shotDict)
        return 'removed'

    else:
        likes.append(uid)
        shotDict.update({'likes': likes})
        await shotRef.update(shotDict)
        return 'added'

async def addView(shotAuthorId: str, shotId: str, uid: str):
    shotRef = db.collection('users').document(shotAuthorId).collection('shots').document(shotId)
    shotSnap = await shotRef.get()
    shotDict: Dict[str, Any] = shotSnap.to_dict()
    views: List[str] = shotDict.get('views')
    views.append(uid)
    shotDict.update({'views': views})
    await shotRef.update(shotDict)
    return 'added'


async def getDrafts(userId: str, asDoc: bool):
    draftRef = db.collection('users').document(userId).collection('shots')
    drafts = await draftRef.get()
    draftsList = []
    for draft in drafts:
        draftData = draft.to_dict()
        if draftData.get('isDraft') == True:
            if asDoc:
                draftData['doc_id'] = draft.id
                draftsList.append(draftData)
            else:
                draftsList.append(draftData)

    draftsList.sort(key=getCreatedDate, reverse=True)
    return draftsList



async def getShots(userId: str, asDoc: bool, limit: Optional[int] = None):
    if not limit:
        shotsRef = db.collection('users').document(userId).collection('shots')
        shots = await shotsRef.get()
        shotsList = []
        for shot in shots:
            shotData: Dict[str, Any] = shot.to_dict()
            if shotData.get('isDraft') == False:
                if (asDoc):
                    shotData['doc_id'] = shot.id
                    shotsList.append(shotData)
                if (not asDoc):
                    shotsList.append(shotData)

        shotsList.sort(key=getCreatedDate, reverse=True)
        return shotsList
    else:
        shotsRefs = db.collection('users').document(userId).collection('shots').where('isDraft', '==', False).order_by('createdAt', 'DESCENDING').limit(count=limit)
        shots = await shotsRefs.get()
        shotsList = []

        for shot in shots:
            shotData: Dict[str, Any] = shot.to_dict()
            if shotData.get('isDraft') == False:
                if (asDoc):
                    shotData['doc_id'] = shot.id
                    shotsList.append(shotData)
                if (not asDoc):
                    shotsList.append(shotData)
        
        shotsList.sort(key=getCreatedDate, reverse=True)
        return shotsList

    # shots = db.collection('users').document(userId).collection('shots').list_documents()
    # shotsList = []
    # async for shot in shots:
    #     data = await shot.get()
    #     shotData: Dict[str, Any] = data.to_dict()
    #     if shotData.get('isDraft') == False:
    #         if (asDoc):
    #             shotData['doc_id'] = data.id
    #             shotsList.append(shotData)
    #         if (not asDoc):
    #             shotsList.append(shotData)

    # return shotsList
async def getAllShots():
    group = db.collection_group('shots')
    shotsSnaps = await group.where('isDraft', '==', False).get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shot.to_dict())

    return shotsList

async def getUpgradedUsersShots(order: str='popular', userId: Optional[str]=None):
    group = db.collection_group('shots')
    shotsSnaps = await group.where('isDraft', '==', False).get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)

    if (order == 'popular'):
        shotsList.sort(key=getViews, reverse=True)
        return shotsList
    if (order == 'following' and userId):
        followingShot = []
        follows = await getFollows(userId=userId)
        for follow in follows:
            shots = await getShots(userId=follow, asDoc=True)
            for shot in shots:
                followingShot.append(shot)
        followingShot.sort(key=getCreatedDate, reverse=True)
        return followingShot
    elif (order == 'new'):
        shotsList.sort(key=getCreatedDate, reverse=True)
        return shotsList
    
    return shotsList

# popular <-> following <-> new
async def getAllUsersShots(order: str='popular', userId: Optional[str]=None):
    userIds = getUsersIdList()
    shotsList = []
    
    for user in userIds:
        shots = await getShots(user, True)
        for shot in shots:
            shotsList.append(shot)

    if (order == 'popular'):
        shotsList.sort(key=getViews, reverse=True)
        return shotsList
    if (order == 'following' and userId):
        followingShot = []
        follows = await getFollows(userId=userId)
        for follow in follows:
            shots = await getShots(userId=follow, asDoc=True)
            for shot in shots:
                followingShot.append(shot)
        followingShot.sort(key=getCreatedDate, reverse=True)
        return followingShot
    elif (order == 'new'):
        shotsList.sort(key=getCreatedDate, reverse=True)
        return shotsList
    
    return shotsList

async def getShot(userId: str, shotId: str):
    shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
    shotSnap = await shotRef.get()
    if shotSnap.exists:
        snapDict = shotSnap.to_dict()
        snapDict['doc_id'] = shotSnap.id
        return snapDict
    else:
        return None

async def getDeleteShot(userId: str, shotId: str):
    shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
    try:
        client = httpx.AsyncClient()
        res = await client.delete(f'{host}/files/folder?link=users/{userId}/{shotId}')
        if res.is_success:
            await shotRef.delete()
            return True
        return False
    except:
        return False