from firebase_admin import firestore
from datetime import datetime
from typing import Any, Dict, List, Optional
from database.files import removeFolder
from firebase import db
from helpers.generators import id_generator
from helpers.shots_categories import getCategory
from schemas.draft import DraftToPublish
from schemas.shot import CommentBlock, ShotData, ShotDataForUpload, NewCommentBlock

def getCreatedDate(el):
    return el['createdAt']

def getViews(el):
    return len(el['views'])

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

async def publishDraft(userId: str, draftId: str, draft: DraftToPublish):
    draftRef = db.collection('users').document(userId).collection('shots').document(draftId)
    draftSnap = await draftRef.get()
    dictDraft = draft.dict()
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
    dictShot = shot.dict()
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
    dictDraft = draft.dict()
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
    if uid in likes:
        filteredLikes = [likerUID for likerUID in likes if likerUID != uid]
        await shotRef.update({'likes': filteredLikes})
        return 'removed'
    else:
        likeDict = {
            'uid': uid,
            'createdAt': datetime.now().timestamp()
        }
        likes.append(likeDict)
        await shotRef.update({'likes': likes})
        return 'added'

async def addView(shotAuthorId: str, shotId: str, uid: str):
    shotRef = db.collection('users').document(shotAuthorId).collection('shots').document(shotId)
    await shotRef.update({
        'views': firestore.ArrayUnion([{
            'uid': uid,
            'createdAt': datetime.now().timestamp()
        }])
    })
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


async def getShots(userId: str, order: Optional[str]='popular', limit: Optional[int] = None, exclude: Optional[str] = None):
    order_by = getViews if order == 'popular' else getCreatedDate
    shotsRef = db.collection('users').document(userId).collection('shots').where('isDraft', '==', False)
    
    shots = await shotsRef.get()
    shotsList = []
    
    for shot in shots:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        if exclude and shot.id not in exclude:
            shotsList.append(shotDict)
        else:
            shotsList.append(shotDict)

    shotsList.sort(key=order_by, reverse=True)

    if limit:
        return shotsList[0:limit]

    return shotsList

async def getAllShots():
    shotsRef = db.collection_group('shots').where('isDraft', '==', False)
    shots = await shotsRef.get()
    shotsList = []

    for shot in shots:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)
    
    return shotsList

async def getShotById(shotId: str):
    shots = await getAllShots()
    targetShot = None
    
    for shot in shots:
        if shot['doc_id'] == shotId:
            targetShot = shot

    return targetShot

async def chunkWithOrder(skip: Optional[int], order: str='popular'):
    group = db.collection_group('shots')
    order_by = getViews if order == 'popular' else getCreatedDate

    shotsSnapsQuery = group.where('isDraft', '==', False)

    shotsSnaps = await shotsSnapsQuery.get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)
    
    shotsList.sort(key=order_by if order != 'following' else getCreatedDate, reverse=True)

    if skip != None and skip > -1:
        return shotsList[skip:skip+16]
    return len(shotsList)

async def chunkWithOrderAndCategory(category: str, skip: Optional[int], order: str='popular'):
    group = db.collection_group('shots')
    order_by = getViews if order == 'popular' else getCreatedDate
    tags: List[str] = await getCategory(category)
    shotsSnapsQuery = group.where('isDraft', '==', False).where('tags', 'array_contains_any', tags)

    shotsSnaps = await shotsSnapsQuery.get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)
    
    shotsList.sort(key=order_by if order != 'following' else getCreatedDate, reverse=True)

    if skip != None and skip > -1:
        return shotsList[skip:skip+16]
    return len(shotsList)

async def chunkUserWithOrder(userId: str, skip: Optional[int], order: str='popular'):
    group = db.collection_group('shots')
    order_by = getViews if order == 'popular' else getCreatedDate

    shotsSnapsQuery = group.where('isDraft', '==', False).where('authorId', '==', userId)

    shotsSnaps = await shotsSnapsQuery.get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)
    
    shotsList.sort(key=order_by if order != 'following' else getCreatedDate, reverse=True)
    
    if skip != None and skip > -1:
        return shotsList[skip:skip+16]
    return len(shotsList)

async def getShot(shotId: str, userId: Optional[str]=None):
    if (userId):
        shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
        shotSnap = await shotRef.get()
        if shotSnap.exists:
            snapDict = shotSnap.to_dict()
            snapDict['doc_id'] = shotSnap.id
            return snapDict
        else:
            return None

    else:
        shot = await getShotById(shotId=shotId)
        return shot

async def getDeleteShot(userId: str, shotId: str):
    shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
    try:    
        link_to_obj = f'users/{userId}/{shotId}'
        await shotRef.delete()
        res = await removeFolder(link=link_to_obj)
        return res
    except:
        return False

def removeIdFromComment(comments: List[CommentBlock], idToDelete: str):
    return [comment for comment in comments if comment.get('id') != idToDelete]

async def removeComment(userId: str, shotId: str, commentId: str):
    try:
        shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
        shotSnap = await shotRef.get()
        shotDict = shotSnap.to_dict()
        comments: List[CommentBlock] = shotDict.get('comments')
        filteredComments = removeIdFromComment(comments=comments, idToDelete=commentId)
        await shotRef.update({ 'comments': filteredComments })
        return True
    except:
        return False

async def patchComment(userId: str, shotId: str, comment: CommentBlock):
    pass

async def addComment(userId: str, shotId: str, comment: NewCommentBlock):
        try:
            shotRef = db.collection('users').document(userId).collection('shots').document(shotId)
            shotSnap = await shotRef.get()
            shotDict = shotSnap.to_dict()
            comments: List[CommentBlock] = shotDict.get('comments')
            commentDict = comment.dict()
            commentDict.update({ 'id': id_generator(15) })
            comments.append(commentDict)
            await shotRef.update({ 'comments': comments })
            return True
        except:
            return False
