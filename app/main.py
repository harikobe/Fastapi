from fastapi import FastAPI
from .database import engine
from . import models
from passlib.context import CryptContext
from .routers import users,posts,vote
from . import auth
from .config import settings
#import the middleware
from fastapi.middleware.cors import CORSMiddleware
#used to implement the database orm models in the path operation:
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]


#import the middleware:
app.add_middleware(
     CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#import the routers path operations:
app.include_router(users.router)
app.include_router(posts.router)
#for the authentication of when the user login:
app.include_router(auth.router)
#voting system
app.include_router(vote.router)


@app.get("/")
def root():
     return {"message":"hello world"}