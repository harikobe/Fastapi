#contains password algorithms

from passlib.context import CryptContext


#setting rhe algorithm as bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#hashing function:
def hash(password:str):
    return pwd_context.hash(password)


#function to compare the hashed passwords:
def verify_password(plain_password, hashed_password):
    #the "verify" is to check the hash password
    return pwd_context.verify(plain_password, hashed_password)
