import httpx
from datetime import datetime
from typing import Any, Dict, List, Optional
from database.files import removeFolder
from database.user import getFollows
from firebase import db
from helpers.generators import id_generator
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
    if (uid in likes):
        filteredLikes = []
        for likerUID in likes:
            if likerUID != uid:
                filteredLikes.append(likerUID)
        shotDict.update({'likes': filteredLikes})
        await shotRef.update(shotDict)
        return 'removed'

    else:
        likeDict = {
            'uid': uid,
            'createdAt': datetime.now().timestamp()
        }
        likes.append(likeDict)
        shotDict.update({'likes': likes})
        await shotRef.update(shotDict)
        return 'added'

async def addView(shotAuthorId: str, shotId: str, uid: str):
    shotRef = db.collection('users').document(shotAuthorId).collection('shots').document(shotId)
    shotSnap = await shotRef.get()
    shotDict: Dict[str, Any] = shotSnap.to_dict()
    views: List[str] = shotDict.get('views')
    likeDict = {
        'uid': uid,
        'createdAt': datetime.now().timestamp()
    }
    views.append(likeDict)
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



async def getShots(userId: str, asDoc: bool, order: Optional[str]='popular', limit: Optional[int] = None, exclude: Optional[str] = None):
    order_by = 'views' if order == 'popular' else 'createdAt'
    if not limit:
        shotsRef = db.collection('users').document(userId).collection('shots').where('isDraft', '==', False).order_by(order_by, 'DESCENDING')
        shots = await shotsRef.get()
        shotsList = []
        for shot in shots:
            if exclude:
                if shot.id != exclude:
                    shotData: Dict[str, Any] = shot.to_dict()
                    if shotData.get('isDraft') == False:
                        if (asDoc):
                            shotData['doc_id'] = shot.id
                            shotsList.append(shotData)
                        if (not asDoc):
                            shotsList.append(shotData)
            else:
                shotData: Dict[str, Any] = shot.to_dict()
                if shotData.get('isDraft') == False:
                    if (asDoc):
                        shotData['doc_id'] = shot.id
                        shotsList.append(shotData)
                    if (not asDoc):
                        shotsList.append(shotData)
        return shotsList
    else:
        shotsRef = db.collection('users').document(userId).collection('shots').where('isDraft', '==', False).order_by(order_by, 'DESCENDING')
        shots = await shotsRef.get()
        shotsList = []
        for shot in shots:
            if exclude:
                if shot.id != exclude:
                    shotData: Dict[str, Any] = shot.to_dict()
                    if shotData.get('isDraft') == False:
                        if (asDoc):
                            shotData['doc_id'] = shot.id
                            shotsList.append(shotData)
                        if (not asDoc):
                            shotsList.append(shotData)
            else:
                shotData: Dict[str, Any] = shot.to_dict()
                if shotData.get('isDraft') == False:
                    if (asDoc):
                        shotData['doc_id'] = shot.id
                        shotsList.append(shotData)
                    if (not asDoc):
                        shotsList.append(shotData)
        return shotsList[0:limit]
async def getAllShots(skip: Optional[int]=0, order: str='popular'):
    order_by = 'views' if order == 'popular' else 'createdAt'
    group = db.collection_group('shots').order_by(order_by, 'DESCENDING').limit(16).offset(skip)
    shotsSnaps = await group.where('isDraft', '==', False).get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)

    return shotsList

async def getChunkedShots(order: str='popular', userId: Optional[str]=None, skip: Optional[int]=0):
    group = db.collection_group('shots')
    order_by = 'views' if order == 'popular' else 'createdAt'
    shotsSnapsQuery = group.where('isDraft', '==', False).order_by(order_by, 'DESCENDING').limit(16).offset(skip)
    shotsSnaps = await shotsSnapsQuery.get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)

    return shotsList

async def getUserChunkedShots(userId: str, order: str='popular', skip: Optional[int]=0):
    userShotsRef = db.collection('users').document(userId).collection('shots')
    order_by = 'views' if order == 'popular' else 'createdAt'
    shotsSnapsQuery = userShotsRef.where('isDraft', '==', False).order_by(order_by, 'DESCENDING').limit(16).offset(skip)
    shotsSnaps = await shotsSnapsQuery.get()
    shotsList = []
    
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)

    return shotsList


async def getUpgradedUsersShots(order: Optional[str]='popular', userId: Optional[str]=None):
    group = db.collection_group('shots')
    order_by = 'views' if order == 'popular' else 'createdAt'
    shotsSnaps = await group.where('isDraft', '==', False).order_by(order_by, 'DESCENDING').get()
    shotsList = []
    for shot in shotsSnaps:
        shotDict = shot.to_dict()
        shotDict.update({ 'doc_id': shot.id })
        shotsList.append(shotDict)

    if (order == 'following' and userId):
        followingShot = []
        follows = await getFollows(userId=userId)
        for follow in follows:
            shots = await getShots(userId=follow, asDoc=True)
            for shot in shots:
                followingShot.append(shot)
        followingShot.sort(key=getCreatedDate, reverse=True)
        return followingShot
    
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
        link_to_obj = f'users/{userId}/{shotId}'
        await shotRef.delete()
        res = await removeFolder(link=link_to_obj)
        return res
    except:
        return False

def removeIdFromComment(comments: List[CommentBlock], idToDelete: str):
    resList = []
    for comment in comments:
        if comment.get('id') != idToDelete:
            resList.append(comment)

    return resList

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
