from pydantic import BaseModel


class CommentCreate(BaseModel):
    post_id: int
    text: str


class CommentOut(BaseModel):
    id: int
    post_id: int
    user_id: int
    text: str

    class Config:
        from_attributes = True
