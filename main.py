import uvicorn
from fastapi import FastAPI

from app.views import users, payments
from app.instance.config import Settings


settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)
app.include_router(users.app, tags=["Users"])
app.include_router(payments.router, tags=["Payments"])


@app.get("/api/healtcheck")
def root():
    return {"message": "The API is On!"}


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
