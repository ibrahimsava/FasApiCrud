from pydantic import BaseModel, Field


class UserCreateReq(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=255)


class UserUpdateEmailReq(BaseModel):
    email: str = Field(min_length=5, max_length=255)