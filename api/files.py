from typing import Optional
from fastapi import APIRouter, UploadFile
from database.files import removeByLink, uploadFileFromString
from uuid import uuid4 as v4

router = APIRouter(
    prefix='/files',
    tags=['Файлы']
)

def setupFilename(filename: str, specialName: Optional[str]=None, prefix: Optional[str]=None):
    splittedName = filename.split('.')
    fileType = splittedName[-1]
    if specialName:
        return f'{specialName}.{fileType}'
    else:
        if prefix:
            return f'{prefix}-{v4()}.{fileType}'
        else:
            return f'{v4()}.{fileType}'
def generateLink(link: str, filename: str):
    if link.startswith('users'):
        if link.endswith('/'):
            return f'{link}{filename}'
        else:
            return f'{link}/{filename}'
    else:
        if link.endswith('/'):
            return f'users/{link}{filename}'
        else:
            return f'users/{link}/{filename}'
@router.post('/file')
async def postFile(link: str, file: UploadFile):
    filename = setupFilename(filename=file.filename, prefix='original')
    db_link = generateLink(link=link, filename=filename)
    bytes = await file.read()
    res = await uploadFileFromString(file=bytes, link=db_link)
    cdn = f'https://cdn.darkmaterial.space/{db_link}'
    return db_link

@router.delete('/file')
async def deleteFile(link: str):
    res = await removeByLink(link)
    return res