from sqlalchemy.orm import Session
from fastapi import HTTPException ,status
from typing import Optional
from . import models,schemas
from datetime import datetime
import hashlib
from fastapi import Depends
from sqlalchemy import or_
from project.core.auth import hash_password


#copy
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
def get_all(db:Session,skip:int,limit:int):
    return db.query(models.User).all()

#To get delete Single user
def delete_user(db: Session, db_user: models.User):
    db.delete(db_user)
    db.commit()
    return db_user
#To create a user after opt verfication
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
    db_user_role = models.UserRole(user_id=user_id, role_id=role_id)
    db.add(db_user_role)
    db.commit()
    db.refresh(db_user_role)
    return db_user_role





#To Update User Details and Role
def update_user_data(db: Session,user_id: int, user: schemas.UpdateUserSchema ):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name=user.name
        db_user.password=user.password
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return {"detail":"User not found"}


#To Update User Details and Role
def update_role_date(db: Session, user_id: int, user: schemas.UpdateUserSchema):
    role_name = user.roles
    
    role = db.query(models.Role).filter(models.Role.name == role_name).first()
    user=db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        if role:
            user_role = db.query(models.UserRole).filter(
                models.UserRole.user_id == user_id
            ).first()
            
            if user_role:
                user_role.role_id = role.id
            else:
                new_user_role = models.UserRole(user_id=user_id, role_id=role.id)
                db.add(new_user_role)
            
            db.commit()
            return {"detail": "Updated successfully"}
        else:
            return {"detail": "Role not found"}
    else:
        return {"detail": "User not found"}
    


    
#To get Role already exists are not
def get_role(db: Session, role_name: str):
    return db.query(models.Role).filter(models.Role.name == role_name).first()



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
#to update the otp for email verfication for forgetpassword
def Update_otp(db: Session, email: str, hash_otp: str ,expire_at:datetime):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        user.otp=hash_otp 
        user.expires_at=expire_at
        db.commit()
        db.refresh(user)
        return user
    return {"message":"User not Found"}
#To Vlaidate otp
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

