from sqlalchemy.orm import Session
from fastapi import HTTPException ,status
from typing import Optional
from . import models,schemas
from datetime import datetime
import hashlib
from fastapi import Depends
from sqlalchemy import or_
from project.core.auth import hash_password
from typing import List, Dict


###copy
def Check_user_email(db:Session,email:str):
    user=db.query(models.User).filter(models.User.email==email).first()
    return user

def Check_user_Phone_number(db:Session,phone_number:str):
    user=db.query(models.User).filter(models.User.phone_number==phone_number).first()
    return user
def update_refresh_token(db:Session,refresh_token:str,id:int):
   
   user=db.query(models.User).filter(models.User.id==id).first() 
   if user:
    user. refresh_token=refresh_token
    db.commit()
    db.refresh(user)
   else:
      print("no")
   return user
def Check_exist_user_id(db:Session,id:str):
    user=db.query(models.User).filter(models.User.id==int(id)).first()
    return user

#To Logout and Delete Refresh Token
def delete_refresh_token(db:Session,user_id:int):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if user:
        user.refresh_token=""
        db.commit()
        db.refresh(user)
        return user

#endcopy


#to check Already exists to create Account
def email_Phone_number_exists(email: str, phone_number: int, db: Session):
    user = db.query(models.User).filter(or_(models.User.email == email, models.User.phone_number == phone_number)).first()
    return user

#To check the email for Forget password
def email_exists(db: Session,email: str ):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

#To get Single user
def get_user(db:Session,user_id:int):
    return db.query(models.User).filter(models.User.id==user_id).first()

#To get all user
def get_all_user(db: Session, skip: int , limit: int):
    return db.query(models.Role).offset(skip).limit(limit).all()


#To get delete Single user
def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()
    return db_user
#To create a user after opt verification
def Create_user(db:Session,user:schemas.UserCreate):
    db_user=models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



#To Create User With Role
def create_user_role(db: Session, user: schemas.User_role):
    hashed_password = hash_password(user.password)
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number
    )
    
    db.add(new_user)
    db.commit()
    
    db.refresh(new_user)
    return new_user.id

#To add a user_id and role_id in create_UserRole Table
def update_user_role(db: Session, user_id: int, role_id: int):
    stmt = models.user_role.insert().values(user_id=user_id, role_id=role_id)
    db.execute(stmt)
    db.commit()
    
    # Optionally, if you want to return the inserted values, you can query the table:
    db_user_role = db.query(models.user_role).filter(
        models.user_role.c.user_id == user_id,
        models.user_role.c.role_id == role_id
    ).first()
    
    return db_user_role





#To Update User Details and Role
def update_user_data(db: Session,user_id: int, user: schemas.UpdateUserSchema ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    hashed_password=hash_password(user.password)
    if db_user:
        db_user.name=user.name
        db_user.password=hashed_password
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return {"detail":"User not found"}


#To Update User Details and Role

def update_role_date(db: Session, user_id: int, user: schemas.UpdateUserSchema):
    role_name = user.roles
    # Fetch the role based on the role name
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        return {"detail": "Role not found"}
    # Fetch the user based on user ID
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"detail": "User not found"}
    # Check if the user role association exists
    user_role = db.query(models.user_role).filter(
        models.user_role.c.user_id == user_id
    ).first()
    if user_role:
        # Update the existing association
        stmt = models.user_role.update().where(
            models.user_role.c.user_id == user_id
        ).values(role_id=role.id)
        db.execute(stmt)
    else:
        # Create a new association
        stmt = models.user_role.insert().values(user_id=user_id, role_id=role.id)
        db.execute(stmt)
    db.commit()
    return {"detail": "Updated successfully"}
    
#To get Role already exists are not
def get_role(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.name == role_name).first()

#To get a Single Role
def get_role_id(db: Session, role_id: int):
    single_role=db.query(models.Role).filter(models.Role.id == role_id).first()
    if single_role:
        return single_role
    else:
        return{"detail": "Role not found"}

#To get all Role
def get_all_roles(db: Session, skip: int, limit: int ):
    return db.query(models.Role).offset(skip).limit(limit).all()

    
#TO get Role already exists are Not for Delete
def get_role_delete(db: Session, role_name: str):
    role=db.query(models.Role).filter(models.Role.name == role_name).first()
    if role:
        return role
    else:
        return {"detail": "Role not found"}
    
#To delete Role
def delete_role_id(db: Session, db_role:int ):
    role=db.query(models.Role).filter(models.Role.id == db_role).first()
    db.delete(role)
    db.commit()
    return {"message": "Role deleted successfully"}

def update_role_name(db: Session, role_id: int, new_name: str):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if role:
        role.name = new_name
        db.commit()
        db.refresh(role)
    return role



#To check user for forget user 
def ResetPassword(db:Session,user_id:int ,hash_Pwd:str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    user.password = hash_Pwd
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
#to update the otp for email verification for forgetpassword
def Update_otp(db: Session, email: str, hash_otp: str ,expire_at:datetime):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        user.otp=hash_otp 
        user.expires_at=expire_at
        db.commit()
        db.refresh(user)
        return user
    return {"message":"User not Found"}
#To Validate otp
def Otp_check(db:Session,OTP=str):
   hashed_otp=hashlib.sha256(str(OTP).encode()).hexdigest()
   user=db.query(models.User).filter(models.User.otp==hashed_otp).first()
   return  user

#To create Role
def create_roles(db:Session,name:str):
    role_check=db.query(models.Role).filter(models.Role.name==name).first()
    if role_check:
        return False
    else:
        role=models.Role(name=name)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role




#To create a Permission 
def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = models.Permission(action=permission)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

#To get all Permission
def get_all_permissions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Permission).offset(skip).limit(limit).all()
# To check the permission exists or not
def get_permission_exists(db: Session, permission_action: str):
    single_permission=db.query(models.Permission).filter(models.Permission.action == permission_action).first()
    if single_permission:
        print(single_permission)
        return single_permission
#To get single Permission
def get_permission_data(db:Session,permission_id:int):
    permission_data=db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    return permission_data
# to delete the permission 

def delete_permission_id(db: Session, db_permission_id:int ):
    permission=db.query(models.Permission).filter(models.Permission.id == db_permission_id).first()
    db.delete(permission)
    db.commit()
    return {"message": "Permission  deleted successfully"}

#To Update a Permission_name
def update_permission_name(db: Session, permission_id: int, new_action: str):
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if permission:
        permission.action = new_action
        db.commit()
        db.refresh(permission)
    return permission

#TO create the Role With Permission 
def assign_permissions_to_role(db: Session, role_name: str, permissions: List[schemas.PermissionBase]):
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    if not role:
        return {"success": False, "message": "Role not found"}

    for perm in permissions:
        action = perm.action
        subject_class = perm.subject_class

        # Check if the permission already exists
        permission = db.query(models.Permission).filter(
            models.Permission.action == action
        ).first()

        if not permission:
            return {"success": False, "message": f"Permission '{action}' for subject '{subject_class}' not found"}

        # Check if this permission is already associated with the role
        association = db.query(models.role_permissions).filter(
            models.role_permissions.c.role_id == role.id,
            models.role_permissions.c.permission_id == permission.id
        ).first()

        if not association:
            # Insert new record in role_permissions table
            stmt = models.role_permissions.insert().values(
                role_id=role.id,
                permission_id=permission.id,
                subject_class=subject_class
            )
            db.execute(stmt)

    # Commit the changes to the database
    db.commit()
    return {"success": True, "message": "Permissions assigned successfully"}
