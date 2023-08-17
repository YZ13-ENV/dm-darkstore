import aioredis 
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_utils.tasks import repeat_every
import httpx
from api.shot import router as ShotRouter
from api.user import router as UserRouter
from api.auth import router as AuthRouter
from api.search import router as SearchRouter
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI(docs_url=None, redoc_url=None)
# app = FastAPI()


origins = [
    'https://design.darkmaterial.space',
    'https://api.storage.darkmaterial.space',
    'https://darkmaterial.space',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ShotRouter)
app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(SearchRouter)

@app.on_event('startup')
@repeat_every(seconds=60 * 10)
async def wakeUpServer():
    response = httpx.get('https://api.storage.darkmaterial.space/')
    if response.is_success:
        print('i woke up api storage server')
    else:
        print(f"Couldn't wake up {response.status_code}")

@app.on_event('startup')
async def startup_event():
    load_dotenv()
    redis = aioredis.from_url(f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}", encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis=redis), prefix='fastapi-cache')

@app.get('/')
def HI_API():
    return 'Hi from DM API!'