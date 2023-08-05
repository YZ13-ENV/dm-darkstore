from datetime import datetime
from firebase import db
from schemas import DraftShotData, ShotData
from helpers import checkShortData, getShortData, getUserDrafts, getUserShotWithDocId, getUserShots, getUserShotsWithDocId, getUsersIdList
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def hello_world():
    return 'Hello, World!'



@app.get('/api/check')
async def checkAPI():
    return 'ok'

@app.get('/api/short')
async def updateShortData(userId: str):
    shortData = await getShortData(userId)
    return shortData


@app.get('/api/shot')
async def getShotById(userId: str, shotId: str):
    await checkShortData(userId)
    shot = await getUserShotWithDocId(userId=userId, shotId=shotId)
    return shot

@app.patch('/api/shot')
async def updateShotById(userId: str, shotId: str, shot: ShotData):
    await checkShortData(userId)
    shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
    updatedSnap = shotRef.update(shot)
    return updatedSnap

@app.get('/api/draft')
async def getDraft(userId: str, draftId: str):
    await checkShortData(userId)
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    draftSnap = await draftRef.get()
    if (draftSnap.exists):
        return draftSnap.to_dict()
    else:
        return None

@app.post('/api/publish')
async def publishDraft(userId: str, draftId: str, draftToPublish: ShotData):
    await checkShortData(userId)
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    await draftRef.set(draftToPublish.dict())
    return True


@app.post('/api/draft')
async def uploadDraft(userId: str, draftId: str, draft: DraftShotData):
    await checkShortData(userId)
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

@app.get('/api/list')
async def getShotsBy(userId: str, drafts: bool):
    await checkShortData(userId)
    if (drafts):
        drafts = await getUserDrafts(userId)
        return drafts
    else :
        shots = await getUserShots(userId)
        return shots


@app.get('/api/shotsDocList')
async def getDocShotsBy(userId: str, noDrafts: bool=False):
    await checkShortData(userId)
    shots = await getUserShotsWithDocId(userId, noDrafts)
    return shots

@app.get('/api/allShots')
async def getAllUsersShots():
    usersIds = await getUsersIdList()
    shotsList = []

    for user in usersIds:
        shots = await getUserShotsWithDocId(user, True)
        for shot in shots:
            shotsList.append(shot)
            
    
    return shotsList