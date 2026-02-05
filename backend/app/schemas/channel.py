from pydantic import BaseModel


class ChannelCreate(BaseModel):
    name: str
    handle: str
    avatar_url: str
    banner_url: str
    bio: str


class ChannelOut(BaseModel):
    id: int
    name: str
    handle: str
    avatar_url: str
    banner_url: str
    bio: str
    is_verified: bool
    subscribers_count: int

    class Config:
        from_attributes = True
