from datetime import timedelta
from io import BytesIO
from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
from PIL import Image
from firebase import storage
from fastapi_cache.decorator import cache
import httpx
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
        "width": 360,
        "height": 280 
    }
]

def getShotImageType(width: int):
    if width == 1280:
        return 'desktop'
    elif width == 640:
        return 'mobile'
    else:
        return 'thumbnail'
def isGifResampling(filename: str):
    if '.gif' in filename:
        return Image.BOX
    else:
        return Image.BILINEAR

def isGif(filename: str):
    if '.gif' in filename:
        return True
    else:
        return False
def getImageType(fileName: str):
    if '.png' in fileName:
        return '.png'
    elif '.jpg':
        return '.jpg'
    return None
        


@router.get('/file')
@cache(expire=120)
async def getFileLink(link: str):
    url = storage.blob(link).generate_signed_url(expiration=timedelta(hours=2))
    return url

@router.get('/profileImage')
# @cache(expire=60)
async def getImageFile(link: str):
    if (os.path.exists(path=link)):
        return FileResponse(path=link)
    else:
        imageType = getImageType(link)
        if imageType:
            splitted = link.split('/')
            joined = '/'.join(splitted[slice(-1)])
            os.makedirs(joined, exist_ok=True)
            storage.blob(link).download_to_filename(filename=link, raw_download=True)
            return FileResponse(path=link)
        return None

@router.post('/uploadMediaInDraft')
async def uploadMedia(file: UploadFile, uid: str, draftId: str):
    if '.mp4' in file.filename:
        link = f"users/{uid}/{draftId}/{file.filename}"
        storage.blob(link).upload_from_file(file.file)
        return link
    else:
        image = Image.open(fp=file.file, mode='r')
        local_link = f"images/{file.filename}"
        link = f"users/{uid}/{draftId}/{file.filename}"
        image.save(fp=local_link, save_all=isGif(file.filename))

        with open(local_link, 'rb') as saved_file:
            storage.blob(link).upload_from_file(saved_file)
            saved_file.close()
        os.remove(local_link)
        return link

@router.post('/uploadThumbnail')
async def uploadThumbnail(file: UploadFile, uid: str, draftId: str):
    size_defined = 720, 405
    if '.mp4' in file.filename:
        return None
    else:
        try:
            print(isGifResampling(file.filename), isGif(file.filename))
            if isGif(file.filename):
                image = Image.open(fp=file.file, mode='r')
                image.resize(size=size_defined, resample=isGifResampling(file.filename))
                db_link = f"users/{uid}/{draftId}/{size_defined[0]}x{size_defined[1]}{file.filename}"
                local_link = f"images/{size_defined[0]}x{size_defined[1]}{file.filename}"
                image.save(local_link, save_all=isGif(file.filename))
            else:
                image = Image.open(fp=file.file, mode='r')
                image.thumbnail(size=size_defined, resample=isGifResampling(file.filename))
                db_link = f"users/{uid}/{draftId}/{size_defined[0]}x{size_defined[1]}{file.filename}"
                local_link = f"images/{size_defined[0]}x{size_defined[1]}{file.filename}"
                image.save(local_link, save_all=isGif(file.filename))

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