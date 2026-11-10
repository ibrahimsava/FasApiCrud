from pydantic import BaseModel

from dto.user_dto import UserDTO


class UserRes(BaseModel):
    id: int
    username: str
    email: str

    @classmethod
    def from_dto(cls, dto: UserDTO) -> "UserRes":
        return cls(id=dto.id, username=dto.username, email=dto.email)


class MessageRes(BaseModel):
    detail: str