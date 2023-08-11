from datetime import timedelta
from io import BytesIO
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
@cache(expire=7200)
async def getFileLink(link: str):
    url = storage.blob(link).generate_signed_url(expiration=timedelta(hours=2))
    return url

@router.post('/uploadThumbnail')
async def uploadThumbnail(file: UploadFile, uid: str, draftId: str):
    images = {}
    for size in sizes:

        size_defined = size.get('width'), size.get('height')
        image = Image.open(fp=file.file, mode='r')
        image.thumbnail(size_defined)
        db_link = f"users/{uid}/{draftId}/{size.get('width')}x{size.get('height')}{file.filename}"
        local_link = f"images/{size.get('width')}x{size.get('height')}{file.filename}"
        image.save(local_link)

        imageRef = {
            "width": size.get('width'),
            "height": size.get('height'),
            'link': db_link
        }

        images.update({ getShotImageType(size.get('width')): imageRef })
        with open(local_link, 'rb') as saved_file:
            storage.blob(db_link).upload_from_file(saved_file)
            saved_file.close()
        os.remove(local_link)
    return images