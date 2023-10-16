from fastapi import APIRouter
from firebase import db
from schemas.note import Note

router = APIRouter(
    prefix='/notes',
    tags=['Заметки']
)

@router.get('/all')
async def getAllNotes(userId: str):
    notesCollection = db.collection('users').document(userId).collection('notes')
    notesSnaps = await notesCollection.get()

    list = []

    for note in notesSnaps:
        noteDict = note.to_dict()
        noteDict.update({ 'doc_id': note.id })
        list.append(noteDict)

    return list

@router.get('/note/{noteId}')
async def getNoteById(userId: str, noteId: str):
    noteRef = db.collection('users').document(userId).collection('notes').document(noteId)
    noteSnap = await noteRef.get()
    if noteSnap.exists:
        noteDict = noteSnap.to_dict()
        # noteDict.update({ 'doc_id': noteSnap.id })
        return noteDict
    else: return None

@router.post('/note/{noteId}')
async def postNoteById(userId: str, noteId: str, note: Note):
    try:
        noteCollection = db.collection('users').document(userId).collection('notes')
        noteDict = note.dict()
        await noteCollection.add(document_data=noteDict, document_id=noteId)
        return True
    except:
        return False
    
@router.patch('/note/{noteId}')
async def patchNoteById(userId: str, noteId: str, note: Note):
    try:
        noteRef = db.collection('users').document(userId).collection('notes').document(noteId)
        noteDict = note.dict()
        noteSnap = await noteRef.get()
        if noteSnap.exists:
            await noteRef.update(field_updates=noteDict)
            return True
        else: 
            return False
    except:
        return False
    
@router.delete('/note/{noteId}')
async def deleteNoteById(userId: str, noteId: str):
    try:
        noteRef = db.collection('users').document(userId).collection('notes').document(noteId)
        await noteRef.delete()
        return True
    except:
        return False