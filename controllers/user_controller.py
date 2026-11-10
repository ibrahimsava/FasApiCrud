from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from req.user_req import UserCreateReq, UserUpdateEmailReq
from res.user_res import MessageRes, UserRes
from services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/", response_model=UserRes, status_code=status.HTTP_201_CREATED)
def create_user(req: UserCreateReq, service: UserService = Depends(get_user_service)):
    return UserRes.from_dto(service.create(req))


@router.get("/", response_model=list[UserRes])
def list_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
    return [UserRes.from_dto(u) for u in service.get_all(skip, limit)]


@router.get("/username/{username}", response_model=UserRes)
def get_user_by_username(username: str, service: UserService = Depends(get_user_service)):
    return UserRes.from_dto(service.get_by_username(username))


@router.get("/{user_id}", response_model=UserRes)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return UserRes.from_dto(service.get_by_id(user_id))


@router.put("/{user_id}", response_model=UserRes)
def update_user_email(user_id: int, req: UserUpdateEmailReq, service: UserService = Depends(get_user_service)):
    return UserRes.from_dto(service.update_email(user_id, req))


@router.delete("/{user_id}", response_model=MessageRes)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    service.delete(user_id)
    return MessageRes(detail="User deleted successfully")