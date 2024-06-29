from fastapi import APIRouter,Depends,HTTPException,status
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
async def create_role(name:schemas.Role,db:Session=Depends(get_db)):
    name=name.name

    if crud.create_roles(db,name):

        return f"{name} Role Created Successfully"
    
    return {'message':f"{name} Role is Already Exists"}

#to delete user
@router.delete("/delete/")
async def delete_role(role_name:str, db: Session = Depends(get_db)):
    role=crud.get_role(db,role_name)
    if not role :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return crud.delete_role_id(db, role.id)


#To get the Single User
@router.get("single/{role_id}")
async def single_role(role_id:int,db:Session=Depends(get_db),current_user=Depends(auth.get_current_user)):
    role=crud.get_role_id(db,role_id)
    return role

#TO get All Roles
@router.get("/all")
async def all_roles(skip:int=0 ,limit:int=100 ,db:Session=Depends(get_db),current_user=Depends(auth.get_current_user)):
    roles=crud.get_all_roles(db,skip,limit)
    if roles:
        return roles
    else:
        return{"Message":"No Role Create"}