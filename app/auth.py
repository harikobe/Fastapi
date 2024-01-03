#for user authentication: 
# (here all are upto the creating the token for user)

from fastapi import APIRouter,HTTPException,Response,status,Depends
from sqlalchemy.orm import Session
from . import database, oauth2,schemas,models,utils
#import the built in security 
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(tags=['Authentication'])


#creating the login
@router.post("/login")
#         user_credentials:schemas.UserLogin (instead for this)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db: Session=Depends(database.get_db)):

    #create an query that filter to retrieve the user by checking email
    user= db.query(models.User).filter(models.User.email==user_credentials.username).first()
    
    if not user:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Invalid Credentials")
    
    #verify the passowrd: (for this the function has been done in the utils.py)
    # here "user_credentials.password" = plain password,
    # "user.password"=hashed password
    if not utils.verify_password(user_credentials.password,user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail="Invalid credentials")
         
     
    #create an token:
    access_token = oauth2.create_access_token(data={"user_id":user.id})# here the "data" is an payload
     
     
    return{"access_token":access_token,"token_type":"bearer"}

