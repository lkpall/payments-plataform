import uvicorn
from fastapi import FastAPI

from app.infrastructure.db import SessionDep
from app.instance.config import Settings
from app.scripts.init_db import CREATE_USER_TYPE
from app.views import users, payments


settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)
app.include_router(users.app, prefix=f'/api/{settings.VERSION}', tags=["Users"])
app.include_router(payments.router, prefix=f'/api/{settings.VERSION}', tags=["Payments"])


@app.get(f"/api/{settings.VERSION}/healtcheck")
async def root():
    return {"message": "The API is On!"}


@app.get(f'/api/{settings.VERSION}/setup_db')
async def setup_db(session: SessionDep):
    await session.exec(CREATE_USER_TYPE)
    await session.commit()
    return {"message": "db init!"}


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
