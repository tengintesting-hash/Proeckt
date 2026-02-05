from fastapi import APIRouter
from app.api.routes import auth, channels, posts, feed, comments, reactions, subscriptions, admin, media, ads

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(channels.router, prefix="/channels", tags=["channels"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(reactions.router, prefix="/reactions", tags=["reactions"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
api_router.include_router(ads.router, prefix="/ads", tags=["ads"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
