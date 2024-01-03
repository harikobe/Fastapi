from pydantic import BaseModel,Field,EmailStr,conint
from typing import Annotated,Optional
from datetime import datetime #for setting the datetime
from . import models
     
#for creating the posts:
class PostBase(BaseModel):
     title:str
     content:str
     published:bool=True
     
     
class PostCreate(PostBase):
     pass

#----------------------------
#response for the user:
class UserOut(BaseModel):
     id:int
     email:EmailStr
     created_at:datetime
     
     class Config:
          from_attributes=True
                          
#--------------------------------
           
#for sending the response to the user:
class Post(PostBase):
     id:int
     owner_id:int
     created_at:datetime
     #imported the pydantic model "UserOut"
     owner:UserOut
     
     class Config:
          from_attributes=True
          

#response of the post for uesrs:
class PostOut(BaseModel):
     Post:Post
     votes:int
     
     class Config:
          from_attributes=True
     
#------------------------------------

#user registering:
class UserCreate(BaseModel):
     email:EmailStr=Field(unique=True)
     password:str

                       
#--------------------------
            
#user authentication:
                                                       
#User Login:
class UserLogin(BaseModel):
     email:EmailStr
     password:str
     
#---------------------------------------     
     
#JWT Access Token:
class Token(BaseModel):
     access_token:str
     token_type:str
     

#token data:
class TokenData(BaseModel):#details can be given to the payload
     id:Optional[str]
     
     
#---------------------------------------
#for the voting system:

class Vote(BaseModel):
     post_id:int
     #dir - means 1=> liked  0=>not liked or remove the vote
     dir:conint(le=1)

