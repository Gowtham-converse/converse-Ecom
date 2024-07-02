from functools import wraps
from fastapi import HTTPException
from sqlalchemy.orm import Session
from project.models import User,UserRole

def authorize(allowed_permissions: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            db:Session=kwargs.get('db')
            user = kwargs.get("current_user")
            id=user.id
            user=db.query(User).filter(User.id==id).first()
            role=db.query(UserRole).filter(UserRole.user_id==user.id)
            
           
            if  not name or not name.name in allowed_permissions:
                raise HTTPException(status_code=403, detail="User is not authorized to access")
            return await func(*args, **kwargs)
        return wrapper
    return decorator