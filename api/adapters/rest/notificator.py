from fastapi import APIRouter, Request, Depends, Response

from api.app.listener import Listener

from api.ports.firestore.db_main import DBMainFirestore
from api.utils.service_exception_handler import ControllerExceptionHandler

router = APIRouter()
listener = Listener(DBMainFirestore())
listener.get_real_time_data()


@router.get("", status_code=200)
@ControllerExceptionHandler.products
async def get_all_products(response_root: Response):
    print(f"Running listener:")
    return {}
