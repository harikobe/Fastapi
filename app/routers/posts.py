
#path for the post CRUD system:

from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse 
from typing import List,Optional
from .. import schemas,models
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2
#for perform arithmetic functions:
from  sqlalchemy import func

router = APIRouter(
     prefix="/posts",#prefix - to set the prefix as "/posts"
     tags=["Posts"]
     )



#get all the posts
@router.get("/",response_model=List[schemas.PostOut])
async def get_all_posts(db: Session = Depends(get_db), 
                        current_user:int = Depends(oauth2.get_current_user),
                        #query parameters:
                        limit: int = 10,
                        skip:int=0,
                        search:Optional[str]=""):
     #"cursor.execute" to apply the SQL statements in the code
     #cursor.execute("""SELECT * FROM posts""")
     #all_post=cursor.fetchall()#fetch all the posts
     #set limit for pagination purpose
     
     #filter(models.post.title.contains(search) => to search the post on title
     #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
      
     """filter(models.Post.owner_id== current_user.id)
     this is for login user only can see their posts"""
     
     #query for sql joins:
     # "models.Vote.post_id" == "models.Post.id"
     post=db.query(
          models.Post,   
          #count the post(id) for total posts  & label for give name for func count as "votes"
          func.count(models.Vote.post_id).label("votes")).outerjoin(               
          models.Vote,#the "models.Post" join with the "models.Vote"
          models.Vote.post_id == models.Post.id#by linking the same id
          #set it as left outer join. 
          ).group_by(#group by posts(id)
          models.Post.id).filter(
          models.Post.title.contains(search)).limit(limit).offset(skip).all()
     
     return post
     



#create posts:
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
     #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
      #                             (post.title,post.content,post.published))
     #new_post=cursor.fetchone()#return the new post
     #conn.commit()
     
     #for register the posts
    # create_post=models.Post(title=post.title,
                      #       content=post.content,
                       #      published=post.published)
     #   also written as
     # Create a new Post instance by unpacking the values from the `post` object.
     print(current_user)
     
     #create the posts and the owner_id is updated to the dictionary
     create_post=models.Post(owner_id=current_user.id ,**post.dict())#unpack the post model as dictionary
     db.add(create_post)#add the create_post to the db
     db.commit()#commit the changes
     db.refresh(create_post)
     
     return create_post
     


#get the specific posts:
@router.get("/{id}",response_model=schemas.PostOut)
def get_posts_by_id(id:int,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id=%s""",(str(id)))#change the "id" as str
    #post=cursor.fetchone(),
    #get_by_id=db.query(models.Post).filter(models.Post.id == id).first()
    
    post=db.query(
          models.Post,   
          #count the post(id) for total posts  & label for give name for func count as "votes"
          func.count(models.Vote.post_id).label("votes")).outerjoin(               
          models.Vote,#the "models.Post" join with the "models.Vote"
          models.Vote.post_id == models.Post.id#by linking the same id
          #set it as left outer join. 
          ).group_by(#group by posts(id)
          models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f"post with id:{id} was not found")
           
    """
     #user can only get their post only:
    if get_by_id.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail="Not Authorized to perform requested Action")
    """
    
    return post
    
    
    
    

#Delete post:
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
     #cursor.execute("""DELETE FROM posts WHERE id=%s returning * """,(str(id),))
     #deleted_post=cursor.fetchone()
     #conn.commit()#commit the changes
     deleted_post=db.query(models.Post).filter(models.Post.id == id)
     
     post=deleted_post.first()#set variable for the query
     
     #if it does not exist:
     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"post with id:{id} doesnt exist")
     
     #this for the user should only delete their posts:
     #the current user in the create posts path
     if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail="Not Authorized to perform requested Action")
     #if it exist:
     deleted_post.delete(synchronize_session=False)
     db.commit()




#update the post:                                                                                                                                                                                  
@router.put("/{id}",response_model=schemas.Post)
def update_posts(id: int,
                 updated_post: schemas.PostCreate,
                 db: Session = Depends(get_db), 
                 current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published=%s WHERE id=%s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updated_post=cursor.fetchone()
    #conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)#check the post with id
     #if index not exists
    post=post_query.first()#grab the single or the first post
    
    #if it not exists:
    if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = "The post of id no: {id} is not found")
    
      #this for the user should only update their posts:
      #the current user in the create posts path
    if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                              detail="Not Authorized to perform requested Action")
    
    #if it exists:
    post_query.update(updated_post.dict(),synchronize_session=False)#update the fields
    
    db.commit()#commit the changes
    
    return post_query.first()#show the updated post
     
    