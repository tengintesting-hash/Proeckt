from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.session import get_db
from app.schemas.comment import CommentCreate, CommentOut
from app.core.deps import get_current_user
from app.models.comment import Comment
from app.models.post import Post

router = APIRouter()


@router.post("/", response_model=CommentOut)
async def create_comment(
    payload: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Post).where(Post.id == payload.post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(post_id=payload.post_id, user_id=current_user.id, text=payload.text)
    db.add(comment)
    post.comments_count += 1
    await db.commit()
    await db.refresh(comment)
    return comment


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    await db.execute(delete(Comment).where(Comment.id == comment_id))
    await db.commit()
    return {"status": "deleted"}
