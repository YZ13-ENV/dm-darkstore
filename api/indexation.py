import aiofiles
from fastapi import APIRouter

from database.files import uploadFileFromString
from database.shot import getUpgradedUsersShots


router = APIRouter(
    prefix='/indexation',
    tags=['Индексация']
)

@router.post('/run')
async def runIndexation():
    shots = await getUpgradedUsersShots('popular')
    linksFromShots = map(lambda shot: f"https://design.darkmaterial.space/{shot.get('authorId')}/{shot.get('doc_id')} \n", shots)
    async with aiofiles.open('sitemap.txt', 'w+', encoding='utf-8') as f:
        await f.write('https://design.darkmaterial.space/ \n')
        for link in linksFromShots:
            await f.write(link)
        f.close()
    try: 
        async with aiofiles.open('sitemap.txt', 'r', encoding='utf-8') as f:
            bytes = await f.read()
            await uploadFileFromString(file=bytes, link='dm/apps/dey/sitemap.txt')
            f.close()
            
        return True
    except:
        return False