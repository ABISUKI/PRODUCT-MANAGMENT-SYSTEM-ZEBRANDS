from fastapi import APIRouter, Request

router = APIRouter()


@router.post("", status_code=200, include_in_schema=False)
@router.post("/", status_code=200)
async def product_management(request: Request):
    body = await request.json()
    print(f"Input: {body}")
    return {}
