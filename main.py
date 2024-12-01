import uvicorn
from fastapi import FastAPI

from app.infrastructure.db import create_db_and_tables
from app.views import users
from app.instance.config import Settings


settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)
app.include_router(users.app, tags=["Users"])


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.get("/api/healtcheck")
def root():
    return {"message": "The API is On!"}


if __name__ == '__main__':
    uvicorn.run("main:app", port=settings.PORT, host=settings.HOST, reload=settings.RELOAD)
