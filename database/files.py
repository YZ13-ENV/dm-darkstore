from boto3 import client
import os
import dotenv

dotenv.load_dotenv()

s3 = client(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    service_name='s3',
    endpoint_url=os.getenv('STORAGE_ENDPOINT')
)

async def readFile(link: str):
    obj = s3.Object(Bucket='dark-material', Key=link)
    res = obj.get()
    data = res['Body'].read()
    print(res)

async def uploadFileFromString(file: bytes, link: str):
    res = s3.put_object(Bucket='dark-material', Key=link, Body=file, StorageClass='STANDARD')
    return res

async def removeByLink(link: str):
    res = s3.delete_object(Bucket="dark-material", Key=link)
    return res

async def removeFolder(link: str):
    try:
        keysForObjects = []
        for key in s3.list_objects(Bucket='dark-material', Prefix=link)['Contents']:
            keysForObjects.append(key['Key'])
        if len(keysForObjects) > 0:
            for key in keysForObjects:
               await removeByLink(key)
        return True
    
    except:
        return False