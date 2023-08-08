from datetime import datetime
from typing import Any, Dict, List, Optional
from database.user import getUsersIdList
from firebase import db
from asyncio import create_task
from schemas.draft import DraftShotData, DraftToPublish
from schemas.shot import CommentBlock, MediaBlock, ShotData, ShotDataForUpload

def getCreatedDate(el):
    return el['createdAt']

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
        'isDraft': False,
        'authorId': userId,
        'title': dictDraft.get('title'),
        'rootBlock': dictDraft.get('rootBlock'),
        'blocks': dictDraft.get('blocks'),
        'createdAt': datetime.today().timestamp(),
        'likes': [],
        'views': [],
        'comments': [],
        'needFeedBack': dictDraft['needFeedBack'],
        'tags': dictDraft['tags'],
        'thumbnail': dictDraft['thumbnail']

    }
    if (draftSnap.exists):
        filledShot.update({'createdAt': draftSnap.get('createdAt')})
        if dictDraft.get('thumbnail') == None:
            filledShot.pop('thumbnail')
            await draftRef.set(filledShot)
        await draftRef.set(filledShot)
        return True
    else:
        return False

async def updateDraft(userId: str, draftId: str, draft: ShotDataForUpload):
    # patch
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    draftSnap = await draftRef.get()
    dictDraft = draft.model_dump()
    filledDraft = {
        'isDraft': True,
        'authorId': userId,
        'title': dictDraft['title'],
        'rootBlock': dictDraft['rootBlock'],
        'blocks': dictDraft['blocks'],
        'createdAt': datetime.today().timestamp()
    }
    if (not draftSnap.exists):
        await draftRef.set(filledDraft)
        return True
    else:
        snapDict = draftSnap.to_dict()
        filledDraft.update({'createdAt': snapDict.get('createdAt')})
        await draftRef.update(filledDraft)
        return True
    
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
        shotsRefs = db.collection('users').limit(count=limit) #.document(userId).collection('shots')
        shots = shotsRefs.get()
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



async def getAllUsersShots():
    userIds = getUsersIdList()
    shotsList = []
    
    for user in userIds:
        shots = await getShots(user, True)
        for shot in shots:
            shotsList.append(shot)
    shotsList.sort(key=getCreatedDate, reverse=True)
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