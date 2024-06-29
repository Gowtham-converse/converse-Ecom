from fastapi import APIRouter,Depends
from project import crud,models,schemas,database
from sqlalchemy.orm import Session
from project.core import config,auth
from project.database import get_db

router = APIRouter(
    prefix="/Role",
    tags=["Role"],
    responses={400: {"message": "Not found"}}
)

@router.post("/create/role")
async def create_role(name:schemas.Role,db:Session=Depends(get_db),current_user=Depends(auth.get_current_user)):
    name=name.name

    if crud.create_roles(db,name):

        return f"{name} Role Created Successfully"
    
    return {'message':f"{name} Role is Already Exists"}


