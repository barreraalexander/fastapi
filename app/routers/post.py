from fastapi import status, HTTPException, Response, Depends, APIRouter

from app import models, schemas, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

from typing import List, Optional


router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)



# @router.get("/")
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
    ):


    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts


# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
#     limit: int = 10,
#     skip: int = 0,
#     search: Optional[str] = ""
#     ):
#     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     return posts

# allows the user to skip certain number of posts
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0):
#     posts = db.query(models.Post).limit(limit).offset(skip).all()
#     return posts


# allows the user to set a limit for number of returns
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10):
#     posts = db.query(models.Post).limit(limit).all()
#     return posts


# only allows user to get their own posts
# @router.get("/", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
#     return posts



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="that shit was not found")

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id,**post.dict())


    print (current_user)


    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="that shit was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()


    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="that shit was not found")


    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")


    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
