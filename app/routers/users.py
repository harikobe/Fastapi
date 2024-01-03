
#path routers for the users 

from fastapi import APIRouter,Depends,HTTPException,status
from .. import schemas,utils,models
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
     prefix="/users",#prefix - to set the prefix as "/users"
     tags=["Users"]
     )



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db: Session=Depends(get_db)):
     
#creating the hash for password:
     #import the utis file:
     hashed_password=utils.hash(user.password)
     #set the hashed password in the user pass:
     user.password=hashed_password 
     
     
     new_user=models.User(**user.dict())#unpack the post model as dictionary
     db.add(new_user)#add the create_post to the db
     db.commit()#commit the changes
     db.refresh(new_user)
     
     return new_user
     

#retrieve user by id:
@router.get("/{id}",response_model=schemas.UserOut)
def get_users_by_id(id:int,db: Session = Depends(get_db)):
    get_by_id=db.query(models.User).filter(models.User.id == id).first()
    if get_by_id == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return get_by_id