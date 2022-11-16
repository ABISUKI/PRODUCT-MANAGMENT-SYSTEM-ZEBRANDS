import uvicorn

from fastapi import FastAPI

from api.adapters.rest import api_router

app = FastAPI()
app.include_router(api_router, prefix="/v1.0")


@app.get("/")
async def health_check():
    return "ready"


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
