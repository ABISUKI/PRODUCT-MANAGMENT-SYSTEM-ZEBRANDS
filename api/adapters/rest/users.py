from fastapi import APIRouter, Request

router = APIRouter()


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201)
async def create_user(request: Request):
    body = await request.json()
    print(f"Create: {body}")
    return {}


@router.get("", status_code=200, include_in_schema=False)
@router.get("/", status_code=200)
async def get_all_users(request: Request):
    print(f"Getting:")
    return {}


@router.get("/{user_id}", status_code=200)
async def get_user(user_id: str):
    print(f"Getting User:{user_id}")
    return {}


@router.put("", status_code=200, include_in_schema=False)
@router.put("/", status_code=200)
async def update_user(request: Request):
    body = await request.json()
    print(f"Update: {body}")
    return {}


@router.delete("", status_code=200, include_in_schema=False)
@router.delete("/", status_code=200)
async def delete_user(request: Request):
    body = await request.json()
    print(f"Delete: {body}")
    return {}
