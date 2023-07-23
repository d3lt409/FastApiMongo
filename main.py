from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.task import task

from decouple import config

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins, allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)


@app.get('/')
async def welcome():
    return {'message': 'Hello World'}

app.include_router(task)
