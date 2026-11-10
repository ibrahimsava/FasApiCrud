from sqlalchemy.orm import Session

from core.exceptions import ConflictException, NotFoundException
from dto.user_dto import UserDTO
from models.user_model import User
from repositories.user_repository import UserRepository
from req.user_req import UserCreateReq, UserUpdateEmailReq


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create(self, req: UserCreateReq) -> UserDTO:
        if self.repo.find_by_username(req.username):
            raise ConflictException("Username already exists")
        if self.repo.find_by_email(req.email):
            raise ConflictException("Email already exists")

        user = self.repo.save(User(username=req.username, email=req.email))
        return UserDTO.model_validate(user)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[UserDTO]:
        return [UserDTO.model_validate(u) for u in self.repo.find_all(skip, limit)]

    def get_by_id(self, user_id: int) -> UserDTO:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserDTO.model_validate(user)

    def get_by_username(self, username: str) -> UserDTO:
        user = self.repo.find_by_username(username)
        if not user:
            raise NotFoundException("User not found")
        return UserDTO.model_validate(user)

    def update_email(self, user_id: int, req: UserUpdateEmailReq) -> UserDTO:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")

        existing = self.repo.find_by_email(req.email)
        if existing and existing.id != user_id:
            raise ConflictException("Email already exists")

        user.email = req.email
        return UserDTO.model_validate(self.repo.save(user))

    def delete(self, user_id: int) -> None:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        self.repo.delete(user)