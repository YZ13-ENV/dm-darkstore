from datetime import datetime
from typing import Any, Dict
from database.user import getUsersIdList
from firebase import db
from schemas.draft import DraftShotData
from schemas.shot import ShotDataForUpload


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


async def updateDraft(userId: str, draftId: str, draft: DraftShotData):
    # patch
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    draftSnap = await draftRef.get()
    dictDraft = draft.dict()
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
        filledDraft['createdAt'] = snapDict['createdAt']
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