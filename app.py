from api.shot import router as ShotRouter
from api.user import router as UserRouter
from api.auth import router as AuthRouter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(docs_url=None, redoc_url=None)
# app = FastAPI()

app.include_router(ShotRouter)
app.include_router(UserRouter)
app.include_router(AuthRouter)

origins = [
    'https://design.darkmaterial.space',
    'https://darkmaterial.space',
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"]
)

@app.get('/')
def HI_API():
    return 'Hi from DM API!'
