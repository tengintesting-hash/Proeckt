from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TelegramAuthRequest(BaseModel):
    init_data: str
