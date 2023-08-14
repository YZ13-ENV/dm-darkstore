from datetime import timedelta
from fastapi import APIRouter, UploadFile
from PIL import Image
from firebase import storage
from fastapi_cache.decorator import cache
import os
router = APIRouter(
    prefix='/images',
    tags=['Картинки']
)
sizes = [
    {
        "width": 1280,
        "height": 720
    }, 
    {
        "width": 640,
        "height": 480
    },
    {
        "width": 320,
        "height": 240 
    }
]

def getShotImageType(width: int):
    if width == 1280:
        return 'desktop'
    elif width == 640:
        return 'mobile'
    else:
        return 'thumbnail'

@router.get('/file')
@cache(expire=120)
async def getFileLink(link: str):
    url = storage.blob(link).generate_signed_url(expiration=timedelta(hours=2))
    return url

@router.post('/uploadMediaInDraft')
async def uploadThumbnail(file: UploadFile, uid: str, draftId: str):
    image = Image.open(fp=file.file, mode='r')
    local_link = f"images/{file.filename}"
    link = f"users/{uid}/{draftId}/{file.filename}"
    image.save(fp=local_link, optimize=True)

    with open(local_link, 'rb') as saved_file:
        storage.blob(link).upload_from_file(saved_file)
        saved_file.close()
    os.remove(local_link)
    return link

@router.post('/uploadThumbnail')
async def uploadThumbnail(file: UploadFile, uid: str, draftId: str):
    try:
        size_defined = 320, 240
        image = Image.open(fp=file.file, mode='r')
        image.thumbnail(size_defined)
        db_link = f"users/{uid}/{draftId}/{size_defined[0]}x{size_defined[1]}{file.filename}"
        local_link = f"images/{size_defined[0]}x{size_defined[1]}{file.filename}"
        image.save(local_link)

        imageRef = {
            "width": size_defined[0],
            "height": size_defined[1],
            'link': db_link
        }

        with open(local_link, 'rb') as saved_file:
            storage.blob(db_link).upload_from_file(saved_file)
            saved_file.close()
        os.remove(local_link)
        return imageRef
    except:
        return None