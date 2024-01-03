from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Boolean
from sqlalchemy.orm import relationship
#for adding the timestamp for the model
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from .database import Base

#posts:
class Post(Base):
     #give the table name:
     __tablename__="posts"
     
     id=Column(Integer,primary_key=True,nullable=False)
     title=Column(String,nullable=False)
     content=Column(String,nullable=False)
     published=Column(Boolean,server_default="TRUE",nullable=False)
     created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
     owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)#"users.id"=> "tablename.columns"

     #creating an relationship:
     owner = relationship("User")
     
#user registration:<=======
class User(Base):
     #tablename
     __tablename__="users"
     id=Column(Integer,primary_key=True,nullable=False)
     #to register the email;
     email=Column(String,nullable=False,unique=True)
     password=Column(String,nullable=False)
     created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
     phone_number=Column(String)
     
#for voting system:
class Vote(Base):
     __tablename__="votes"
     user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)#"users.id"=> "tablename.columns"
     post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)#"posts.id"=> "tablename.columns"
     
     
      