from typing import Optional

from utils.schemas import BaseModel, InclusiveModel


class TokenResponse(InclusiveModel):
    access_token: str
    token_type: str = "Bearer"


class TokenData(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class OpenAPIToken(BaseModel):
    access_token: str
