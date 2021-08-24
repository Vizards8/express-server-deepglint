from schema.base import UserBaseSchema
from pydantic import BaseModel


class AuthDataSchema(BaseModel):
    code: int = 0
    message: str = 'SUCCESS'
    access: str = None
    user_id: int = None
    user: UserBaseSchema = None


class LoginInputSchema(BaseModel):
    username: str
    password: str = None
