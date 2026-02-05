from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.core.deps import get_current_user
from app.models.reaction import Reaction
from app.models.enums import ReactionType
from app.models.post import Post

router = APIRouter()


@router.post("/{post_id}/{reaction_type}")
async def toggle_reaction(
    post_id: int,
    reaction_type: ReactionType,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    result = await db.execute(select(Reaction).where(Reaction.post_id == post_id, Reaction.user_id == current_user.id))
    reaction = result.scalar_one_or_none()
    if reaction and reaction.reaction == reaction_type:
        await db.delete(reaction)
        if reaction_type == ReactionType.like:
            post.likes_count -= 1
        else:
            post.dislikes_count -= 1
    else:
        if reaction:
            if reaction.reaction == ReactionType.like:
                post.likes_count -= 1
            else:
                post.dislikes_count -= 1
            reaction.reaction = reaction_type
        else:
            reaction = Reaction(post_id=post_id, user_id=current_user.id, reaction=reaction_type)
            db.add(reaction)
        if reaction_type == ReactionType.like:
            post.likes_count += 1
        else:
            post.dislikes_count += 1
    await db.commit()
    return {"likes": post.likes_count, "dislikes": post.dislikes_count}
