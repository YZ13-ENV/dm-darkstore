import io
from typing import Optional
from fastapi import APIRouter, UploadFile
from database.files import removeByLink, uploadFileFromString
from uuid import uuid4 as v4
import imageio
import cv2
import tempfile

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
    await uploadFileFromString(file=bytes, link=db_link)
    return db_link

@router.post('/thumbnail')
async def postThumbnail(link: str, file: UploadFile):
    filename = setupFilename(filename=file.filename, prefix='400x300')
    db_link = generateLink(link=link, filename=filename)
    size_defined = 400, 300
    if file.filename.endswith('.mp4'):
        file_bytes = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(0)
            reader = imageio.get_reader(temp_file.name)
            fps = reader.get_meta_data()['fps']

            with tempfile.NamedTemporaryFile(suffix=".mp4") as output_temp_file:
                writer = imageio.get_writer(output_temp_file.name, fps=fps)

                for i, frame in enumerate(reader):
                    frame = cv2.resize(frame, size_defined)
                    writer.append_data(frame)
                writer.close()

                output_temp_file.seek(0)
                video_bytes = output_temp_file.read()
                await uploadFileFromString(file=video_bytes, link=db_link)
                return db_link
    else:
        file_bytes = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
            temp_file.write(file_bytes)
            temp_file.seek(0)
            image = imageio.imread(temp_file.name)
            image = cv2.resize(image, size_defined)
            with tempfile.NamedTemporaryFile(suffix=".png") as output_temp_file:
                imageio.imsave(output_temp_file.name, image)
                output_temp_file.seek(0)
                image_bytes = output_temp_file.read()
                await uploadFileFromString(file=image_bytes, link=db_link)
                return db_link
    
@router.delete('/file')
async def deleteFile(link: str):
    res = await removeByLink(link)
    return res