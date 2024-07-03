from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from project import crud, models, schemas
from project.database import engine,Base,get_db
from project import routers 
from project.routers import User,Role,Permission
from sqlalchemy.orm import configure_mappers



# configure_mappers()
models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(User.router)
app.include_router(Role.router)
app.include_router(Permission.router)


@app.get("/")
def index():
    return "Hi there Welcome"
