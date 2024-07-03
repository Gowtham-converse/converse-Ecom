from functools import wraps
from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from project import models

def authorize(allowed_permissions: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db:Session=kwargs.get('db')
            user = kwargs.get("current_user")

            user_role=db.query(models.user_role).filter(models.user_role.c.user_id==user.id).first()  #get the current user role id
            if not user_role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role not found")
            
            permission_list = db.query(models.role_permissions.c.permission_id, models.role_permissions.c.subject_class).filter(models.role_permissions.c.role_id == user_role.role_id).all()
            permissions = {(permission.permission_id, permission.subject_class) for permission in permission_list} #get the current user permission list
          
            action_id = db.query(models.Permission).filter(models.Permission.action == allowed_permissions[0]).first()
            if not action_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Action not found")

            allowed_permission = (action_id.id, allowed_permissions[1]) #create the allowed permission tuple 
            #print(allowed_permissions)
            if  not user.id or not allowed_permission in permissions:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized to access")
            return await func(*args, **kwargs)
        return wrapper
    return decorator