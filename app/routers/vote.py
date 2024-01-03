#voting system(likes)

from fastapi import APIRouter,Depends,HTTPException,status
from ..  import schemas,database,models,oauth2
from sqlalchemy.orm import Session


router=APIRouter(
     prefix="/vote",
     tags=["Vote"]
     )


@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,
         db:Session=Depends(database.get_db),
         current_user:int=Depends(oauth2.get_current_user)):
     
     #check the post is existed
     post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
     #if not exist:
     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"Post with id:{vote.post_id} doesnt exist")
     
# Query to check if the user has voted on the specified post
     vote_query=db.query(models.Vote).filter(
          # db models post(id)==schema vote(post_id)
          models.Vote.post_id  == vote.post_id,
          #db models vote(user_id)== oauth2(current_user id)
          models.Vote.user_id  == current_user.id)
     
     
        #Check if the user has already voted:
     found_vote=vote_query.first()
        
     # If the user is trying to upvote (dir == 1)
     if (vote.dir == 1): 
          if found_vote:
               raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
          
       # If the user has already voted, raise a conflict exception
          new_vote=models.Vote(post_id=vote.post_id,#schema "vote"
                               user_id=current_user.id) # logined user 
          
          db.add(new_vote)#add the vote
          db.commit()#commit the changes
          
          return {"message":"Successfully added vote"}
     

     
     else:
          #logic for unvote and #if there is no user ,the vote will deleted
          if not found_vote:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
     
          vote_query.delete(synchronize_session=False)
          db.commit()
     
          return {"message":"Successfully deleted vote"}
