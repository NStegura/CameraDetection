from pydantic import EmailStr, BaseModel, UUID4
from fastapi_users import models


class User(models.BaseUser):
    username: str


class UserCreate(models.BaseUserCreate):
    username: str


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass



# class UserOut(BaseModel):
#     id: int
#     username: str
#     avatar: str
#
#
# class Token(BaseModel):
#     id: int
#     token: str
#
#
# class TokenPayload(BaseModel):
#     user_id: int = None
