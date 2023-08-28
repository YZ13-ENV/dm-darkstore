from boto3 import client
import os
import dotenv

dotenv.load_dotenv()

s3 = client(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    service_name='s3',
    endpoint_url=os.getenv('STORAGE_ENDPOINT')
)

async def uploadFileFromString(file: bytes, link: str):
    res = s3.put_object(Bucket='dark-material', Key=link, Body=file, StorageClass='STANDARD')
    return res

async def removeByLink(link: str):
    try:
        s3.delete_object(Bucket="dark-material", Key=link)
        return True
    except:
        return False