from datetime import datetime
from typing import Any, Dict, List, Optional
from database.user import getUsersIdList
from firebase import db
from schemas.draft import DraftShotData
from schemas.shot import CommentBlock, ImageBlock, ShotData, ShotDataForUpload


async def addShotAsDraft(userId: str, shotId: str, shot: ShotDataForUpload):
    # post
    draftRef = db.collection('users').document(userId).collection('shots').document(shotId)
    draftSnap = await draftRef.get()
    dictDraft = shot.dict()
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

async def publishDraft(
        userId: str, draftId: str, draft: DraftShotData,
        needFeedBack: bool, tags: List[str], thumbnail: Optional[ImageBlock]=None
    ):
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
        'needFeedback': needFeedBack,
        'tags': tags,
        'thumbnail': thumbnail.model_dump()

    }
    if (draftSnap.exists):
        filledShot.update({'createdAt': draftSnap.get('createdAt')})
        if thumbnail == None:
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
    return draftsList

async def getShots(userId: str, asDoc: bool):
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
    return shotsList

async def getAllUsersShots():
    userIds = await getUsersIdList()
    shotsList = []

    for user in userIds:
        shots = await getShots(user, True)
        for shot in shots:
            shotsList.append(shot)
    
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