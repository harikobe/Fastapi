#this id for the JWT Token
#here all are upto the 
# creating token logic
# verify for the token 
# current_user func -> used authentication security for every path operation

from  jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

#The oauth2_scheme is an instance of OAuth2PasswordBearer, 
# which is a FastAPI security class for handling
#  OAuth2-style token authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


#for jwt token ,we need:
#SECRET KEY(password that even do know to the users)
#algorithm(signature)
#expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


"""
            " create_access_token "
            generates a JWT token by 
            encoding the provided payload (data) with an expiration time.
""" 
def create_access_token(data:dict): #here"data "is payload in "dict"type
     #copy the data(payload) for dont affect the original data
     to_encode=data.copy()
     
#create an exiparation field:(setting the expire)
     expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
     #update the "expire" into the "to_encode"
     to_encode.update({"exp":expire})
     
     #encode all the (to_encode,SECRET_KEY,algorithms)
     encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
     return encoded_jwt


"""
      "verify_access_token" => decodes a JWT token, 
      extracts the user ID from the payload, and 
      validates it using the TokenData schema.
"""
#it is used to verify the user details 
def verify_access_token(token:str,credentials_exception):
     
     try:
         #decode the token by entering the 3 things:
         payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
           
         #extract the id:  
         id : str = payload.get("user_id")#grab the token by get the users_id and give the variable name as "id"
         
         if id is None:
            raise credentials_exception
     
        #validate the id: 
         token_data=schemas.TokenData(id=str(id)) #checking by comparing the id
         
     except JWTError:
          raise credentials_exception
     
     return token_data


"""
   "get_current_user" is a dependency used in path operations
    to verify the user's authentication by checking the JWT token.
"""
def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
     credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not validate credentials",
                                         headers=({"WWW-Authenticate":"Bearer"}))
     
     #verify the token 
     decoded_token = verify_access_token(token,credentials_exception)
     
     #grab the user from the database
     user=db.query(models.User).filter(models.User.id == decoded_token.id).first()
     
     return user


