from fastapi import FastAPI

from app.routes import users
from app.db.db import create_db_and_tables


app = FastAPI()
app.include_router(users.app)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
