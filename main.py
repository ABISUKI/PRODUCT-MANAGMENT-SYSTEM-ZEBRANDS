import logging

import uvicorn

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from api.adapters.rest import api_router
from api.utils.response import Response
from api.utils.response import Status
from deps import Container

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "products",
        "description": "Operations with product catalog..",
    },
]

description = """
Basic catalog system to manage products. 🚀

## User
You will be able to:
* **Create users**.
* **Read users**
* **Update users**
* **Remove users**

## Products
You will be able to:
* **Create products**.
* **Read products**
* **Update products**
* **Remove products**
"""

container = Container()
app = FastAPI(title="PRODUCT MANAGE SYSTEM ZEBRANDS", description=description, openapi_tags=tags_metadata)
app.include_router(api_router, prefix="/v1.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: Exception):
    response = Response()
    try:
        print(f"Input Body: {exc.body}")
        all_errors = exc.raw_errors[0].exc.errors()
        logging.error(all_errors)
        response.add_error(all_errors)
        response.set_response(Status.BAD_REQUEST, {})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response.result))

    except Exception as error:
        logging.error(str(exc.errors()))
        response.add_error(all_errors)
        response.set_response(Status.BAD_REQUEST, {})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=jsonable_encoder(response.result))


@app.get("/")
async def health_check():
    return "ready"


if __name__ == "__main__":
    uvicorn.run(app, port=8080)