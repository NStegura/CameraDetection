from pydantic import EmailStr
from fastapi_users import models


class User(models.BaseUser):
    username: str
    phone: str


class UserCreate(models.CreateUpdateDictModel):
    username: str
    email: EmailStr
    password: str
    phone: str


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
