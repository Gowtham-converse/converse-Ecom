from fastapi import APIRouter,Depends,HTTPException,status,Body
from project import crud,models,schemas,database
from sqlalchemy.orm import Session
from project.core import config,auth
from project.database import get_db
from typing import List, Dict

router = APIRouter(
    prefix="/Permission",
    tags=["Permission"],
    responses={400: {"message": "Not found"}}
)


#TO Create a permission
@router.post("/permissions/")
async def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    permission=permission.action
    if crud.get_permission_exists(db,permission):
        return{"Message":"Permission name already exists"}
    else:
        return crud.create_permission(db=db, permission=permission)
#To see all The data in Permission
@router.get("/permissions/")
async def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    permissions = crud.get_all_permissions(db, skip=skip, limit=limit)
    return permissions

#To get a  Single permission
@router.get("/{permission_id}")
async def get_permission_single(permission_id:int,db:Session=Depends(get_db)):
    permission=crud.get_permission_data(db,permission_id)
    if permission:
        return permission
    else:
        return {"message":"permission not available"}
    
    
#TO delete the Permission 
@router.delete("/delete")
async def delete_permission(permission_name:str,db:Session=Depends(get_db)):
    permission=crud.get_permission_exists(db,permission_name)
    if permission:
        return crud.delete_permission_id(db,permission.id)
    else:
        return{"Message":f"no permission name '{permission_name}'"}
     
#TO update the Permission 
@router.put("/permission/update/")
def Update_permission_name(exists_permission: str, request: schemas.UpdatePermissionNameRequest, db: Session = Depends(get_db)):
    exists_permission=crud.get_permission_exists(db,exists_permission)
    permission = crud.update_permission_name(db, exists_permission.id, request.new_action)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

#Example usage in your API route or function
@router.post("/roles/assign-permissions/")
def assign_permissions(role_permissions: schemas.RolePermissionsAssign,db: Session = Depends(get_db)):
    result = crud.assign_permissions_to_role(db, role_permissions.role_name, role_permissions.permissions)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result
