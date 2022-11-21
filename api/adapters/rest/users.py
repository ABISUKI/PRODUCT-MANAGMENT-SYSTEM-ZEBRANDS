from fastapi import APIRouter, Request, Depends, Response
from fastapi.security import HTTPBearer, HTTPBasic, HTTPBasicCredentials
from dependency_injector.wiring import inject

from api.app.entities.input_models import UserCreationInput, UserUpdateInput, UserDeleteInput
from api.ports.auth.auth import Auth
from api.app.users import Users
from api.ports.firestore.db_main import DBMainFirestore
from api.utils.service_exception_handler import ControllerExceptionHandler


router = APIRouter()
bearer_auth = HTTPBearer()
basic_security = HTTPBasic()


@router.get("/login", status_code=200, tags=["users"])
@inject
@ControllerExceptionHandler.users
async def login(response_root: Response, credentials: HTTPBasicCredentials = Depends(basic_security), db_firestore: DBMainFirestore = Depends(DBMainFirestore)
):
    login_m = Auth(db_firestore)
    return {"access_token": login_m.login(email=credentials.username, pwd=credentials.password),
            "type": "token"}


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, tags=["users"])
@inject
@ControllerExceptionHandler.users_creation
@Auth.check_access_admin
async def create_user(response_root: Response,
                      request: Request,
                      user_creation_input: UserCreationInput,
                      token: str = Depends(bearer_auth),
                      db_firestore: DBMainFirestore = Depends(DBMainFirestore)
):

    users = Users(db_firestore)
    return users.create_user(user_creation_input)


@router.get("", status_code=200, include_in_schema=False)
@router.get("/", status_code=200, tags=["users"])
@inject
@ControllerExceptionHandler.users
@Auth.check_access_admin
async def get_all_users(response_root: Response,
                        request: Request,
                        token: str = Depends(bearer_auth),
                        db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    print(f"Getting all users:")
    users = Users(db_firestore)
    return users.get_all_users()


@router.get("/{user_id}", status_code=200, tags=["users"])
@inject
@ControllerExceptionHandler.users
@Auth.check_access_admin
async def get_user(response_root: Response,
                   user_id: str,
                   request: Request,
                   token: str = Depends(bearer_auth),
                   db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    print(f"Getting User:{user_id}")
    users = Users(db_firestore)
    return users.get_user_by_id(user_id)


@router.put("", status_code=200, include_in_schema=False)
@router.put("/", status_code=200, tags=["users"])
@inject
@ControllerExceptionHandler.users
@Auth.check_access_admin
async def update_user(response_root: Response,
                      request: Request,
                      user_update_input: UserUpdateInput,
                      token: str = Depends(bearer_auth),
                      db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    users = Users(db_firestore)
    return users.update_user(user_update_input)


@router.delete("", status_code=200, include_in_schema=False)
@router.delete("/", status_code=200, tags=["users"])
@inject
@ControllerExceptionHandler.users
@Auth.check_access_admin
async def delete_user(response_root: Response,
                      request: Request,
                      user_delete_input: UserDeleteInput,
                      token: str = Depends(bearer_auth),
                      db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    users = Users(db_firestore)
    return users.delete_user(user_delete_input)
