from fastapi import APIRouter, Request, Depends, Response
from dependency_injector.wiring import inject

from api.app.entities.input_models import UserCreationInput, UserUpdateInput, UserDeleteInput
from api.app.users import Users
from api.ports.firestore.db_users import DBMainFirestore
from api.utils.service_exception_handler import ControllerExceptionHandler

router = APIRouter()


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201)
@inject
@ControllerExceptionHandler.users_creation
async def create_user(response_root: Response, request: Request, db_firestore: DBMainFirestore = Depends(DBMainFirestore)
):
    body = await request.json()
    print(f"Create: {body}")
    body = UserCreationInput(**body).dict()
    users = Users(db_firestore)
    return users.create_user(**body)


@router.get("", status_code=200, include_in_schema=False)
@router.get("/", status_code=200)
@inject
@ControllerExceptionHandler.users_creation
async def get_all_users(response_root: Response, db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    print(f"Getting all users:")
    users = Users(db_firestore)
    return users.get_all_users()


@router.get("/{user_id}", status_code=200)
@inject
@ControllerExceptionHandler.users
async def get_user(response_root: Response, user_id: str, db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    print(f"Getting User:{user_id}")
    users = Users(db_firestore)
    return users.get_user_by_id(user_id)


@router.put("", status_code=200, include_in_schema=False)
@router.put("/", status_code=200)
@inject
@ControllerExceptionHandler.users
async def update_user(response_root: Response, request: Request, db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    body = await request.json()
    print(f"Update: {body}")
    body = UserUpdateInput(**body).dict()
    users = Users(db_firestore)
    return users.update_user(**body)


@router.delete("", status_code=200, include_in_schema=False)
@router.delete("/", status_code=200)
@inject
@ControllerExceptionHandler.users
async def delete_user(response_root: Response, request: Request, db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    body = await request.json()
    print(f"Deleted: {body}")
    body = UserDeleteInput(**body).dict()
    users = Users(db_firestore)
    return users.delete_user(**body)
