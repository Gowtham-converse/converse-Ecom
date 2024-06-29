from fastapi import APIRouter, Depends, HTTPException,Body,Request,status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import hashlib
from project import crud, schemas, models, database
from project.core import auth
from project.core import config
from project.database import get_db
from typing import Dict
from pydantic import BaseModel,EmailStr
#export
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError


router = APIRouter(
    prefix="/user",
    tags=["users"],
    responses={400: {"message": "Not found"}}
)
# @router.post("/login")
# async def login_form(form_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db),):
#     user = auth.check_exist_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
#     access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
#     refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
#     access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
#     refresh_token = auth.create_refresh_token(data={"sub":str(user.id)}, expires_delta=refresh_token_expires)
#     crud.update_refresh_token(db, refresh_token,user.id) #update the refresh_token to database
#     return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

temp_user_data: Dict[str, dict] = {}

#Get All the Data from  the user and store locally To verify-otp and save user
@router.post("/create-otp")
async def create_user1(user: schemas.User,db:Session=Depends(get_db)):
    global temp_user_data

    if crud.email_Phone_number_exists(user.email,user.phone_number, db):
        return {"message": "Email or Phone number is already Exists"}
    
    else:
        otp_data = config.generate_otp_and_hash()
        otp = otp_data["otp"]
        await config.send_otp_email(user.email, otp)
        
        # Store user data with OTP as key in temp_user_data
        temp_user_data = {
            "email": user.email,
            "name": user.name,
            "otp":otp,
            "hash_otp": otp_data["hash_otp"],
            "otp_ex": otp_data["expiration_time"],
            "phone_number": user.phone_number,
            "password":auth.hash_password(user.password)
        }
        return {"message": "OTP created and sent successfully", "otp": temp_user_data}

#Verify Otp to save the User in Database
@router.put("/verify-otp")
async def verify_otp(otp_data:schemas.UserCreate,db: Session = Depends(get_db)):
    hash_otp_data = temp_user_data.get("hash_otp")
    hash_otp_data1= temp_user_data["hash_otp"]
    print(hash_otp_data)
    print(hash_otp_data1)
    otp_ex = temp_user_data.get("otp_ex")
    email = temp_user_data.get("email")
    name = temp_user_data.get("name")
    phone_number = temp_user_data.get("phone_number")
    password = temp_user_data.get("password")
    if not email:
        raise HTTPException(status_code=400, detail="User data not found")
    new_otp=otp_data.otp
    hash_otp = hashlib.sha256(new_otp.encode()).hexdigest()
    if hash_otp == hash_otp_data:
        if datetime.now() > otp_ex:
            return {'message': 'OTP expired'}
        else:
            existing_user = crud.email_Phone_number_exists(email, phone_number, db)
            if existing_user is None:

                created_user = crud.Create_user(db=db,user=schemas.User(
                        name=temp_user_data["name"],
                        email=temp_user_data["email"],
                        password=temp_user_data["password"],
                        phone_number=temp_user_data["phone_number"]
                    
                ))
                return {"message": "OTP verified successfully and user created", "user":created_user}
            else:
                return {"message": "Email or Phone number is already Exists"}
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP")

#To Login Copy
@router.post("/login")
async def login_token(form_data:schemas.User_Login, db: Session = Depends(get_db),):
    user = auth.check_exist_user(db, form_data.email_or_phonenumber, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    refresh_token = auth.create_refresh_token(data={"sub":str(user.id)}, expires_delta=refresh_token_expires)

    crud.update_refresh_token(db, refresh_token,user.id) #update the refresh_token to database

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

#otp for login
@router.post("/request_otp")
async def login_to_Otp(form_data:schemas.User_LoginBase, db: Session = Depends(get_db)):
    user = auth.check_exist_user_email(db, form_data.email_or_phonenumber)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email")
    else:
       OTP_data=config.generate_otp_and_hash()
       OTP = OTP_data["otp"]
       hash_otp= OTP_data["hash_otp"]
       otp_expiry= OTP_data["expiration_time"]
       await config.send_otp_email(user.email,OTP)
       print(OTP)
       expiry_time = datetime.utcnow() + timedelta(minutes=1)
       # hash and save the otp in database
       print(expiry_time)
       crud.Update_otp(db,form_data.email_or_phonenumber,hash_otp,otp_expiry)
       return HTTPException(status_code=status.HTTP_200_OK,detail="OTP send")

#verify otp and generate token
@router.put("/login")
async def verify_otp_token(otp:schemas.OTP,db:Session=Depends(get_db)):
    user = auth.Check_OTP_valid(db,otp.Otp)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=auth.REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    refresh_token = auth.create_refresh_token(data={"sub": str(user.id)}, expires_delta=refresh_token_expires)

    crud.update_refresh_token(db, refresh_token,user.id) #update the refresh_token to database

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

#To create Acess token by refersh Token
@router.post("/refresh_token/")
async def refresh_token(refresh_token:schemas.refresh_Token,db:Session=Depends(get_db)):
    try:
        access_token=auth.get_access_token_use_refresh_token(refresh_token,db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return access_token

#To check Password
@router.put("/change_password/")
async def change_password(passwords:schemas.change_password,current_user= Depends(auth.get_current_user),db:Session=Depends(get_db)):
     print(passwords.old_password)
     if  not auth.verify_password(passwords.old_password,current_user.password):
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Old password doesn't match!")
     else:
        if passwords.confirm_password != passwords.new_password:
             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail="New passwords and Confirm doesn't match")
        else:
            hash_password=auth.hash_password(passwords.new_password)
            user=crud.ResetPassword(db,current_user.id,hash_password)
            return HTTPException(status_code=status.HTTP_202_ACCEPTED,detail="password Change successfully")
    
#To Logout
@router.delete("/logout/")
async def logout(current_user=Depends(auth.get_current_user),db:Session=Depends(get_db)):
    if current_user.id :
        crud.delete_refresh_token(db,current_user.id)
        return {"message":"Successfully Logout"}
#end copy
#To get Single User
@router.get("/single/user/{user_id}")
async def get_user_single(user_id: int, db: Session = Depends(get_db),current_user=Depends(auth.get_current_user)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

#To get All user
@router.get("/all")
async def get_user_all(skip:int=0,limit:int=100,db:Session=Depends(get_db),current_user=Depends(auth.get_current_user)):
    db_all=crud.get_all(db,skip,limit)
    if db_all is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="DataBase is Empty")
    return db_all

#to delete user
@router.delete("/user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db),current_user=Depends(auth.get_current_user)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return crud.delete_user(db, db_user)

    
#Email Verification for ForgetPassword
@router.put("/email_To_Forget_Password")
async def Email_verify(Eamil:schemas.ResetEmail,db:Session=Depends(get_db)):
    email=Eamil.email
    user = crud.email_exists(db,email) 
    if user:
        otp_data = config.generate_otp_and_hash()
        otp = otp_data["otp"]
        expire_at=otp_data["expiration_time"]
        print(otp)
        await config.send_otp_email(email, otp)
        hash_otp = otp_data["hash_otp"]
        crud.Update_otp(db,email,hash_otp,expire_at)
        print(hash_otp)
        return {"message": "OTP created and sent successfully","details":user,"otp":otp}
    else:
        return {"message": "Email not exists. Sign in first."}
    
@router.post("/otp_verify")
async def Otp_Verify_To_Forget_Password (otp:schemas.ResetOtp,db:Session=Depends(get_db)):
    otp=otp.otp
    user=auth.Check_OTP_valid(db,otp)
    if  user:
        return {"messgae":"OTP verified Successfully","details":user}

@router.put("/Change_Froget_Password")
async def Change_Froget_Password(user:schemas.ResetPassword,Otp:int,db:Session=Depends(get_db)):
    new_password=user.NewPassword
    confirm_password=user.ConfirmPassword

    if new_password == confirm_password:
        hash_Pwd=auth.hash_password(new_password)
        otp=Otp
        # user=db.query(models.User).filter(models.User.otp==otp).first()
        # print(user.email)
        print("thi sspos sioubfd  passsword",otp)
        user_data=auth.Check_OTP_valid(db,otp)
        print("hi jknkinvkisdnivfnsdivfndivfn",user_data.id)
        if  user_data:
            user=user_data.id
            store_date=crud.ResetPassword(db,user,hash_Pwd)
            return {"message":"Password Changed Successfully"}
    return {"message":"New_password and Confirm_password Mismatch"}


@router.post("/create/User_Role")
async def create_user_role(user: schemas.User_role, db: Session = Depends(get_db),current_user=Depends(auth.get_current_user)):
    existing_user = crud.email_Phone_number_exists(user.email, user.phone_number, db)
    if existing_user is None:
        db_user = crud.create_user_role(db, user)
        db_role = crud.get_role(db, user.roles)
        print("roleee ",db_role)
        
        if not db_role:
            raise HTTPException(status_code=404, detail="Role not found")

        # Create user role association
        try:
            d=crud.update_user_role(db, db_user, db_role.id)
            return {"message":"User and Role are created Sucessfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user role: {str(e)}")
    else:
        return {"message": "Email or Phone number is already Exists"}

@router.put("/users/{user_id}")
def update_user(user_id: int, user: schemas.UpdateUserSchema, db: Session = Depends(get_db)):
    
    crud.update_user_data(db,user_id,user)
    d=crud.update_role_date(db,user.roles,user)
    print(d)
    if d:
            response = crud.update_role_date(db, user_id, user)
    return response
    # return {"message":"User and Role are created Sucessfully","d":d}






        # return {"message": "User updated successfully"}
    
    
    

    
    
    # try:
    #     d=crud.create_user_role(db, user_id, db_role.id)
    #     return {"message":"User and Role are created Sucessfully"}
    # except Exception as e:
    # #     raise HTTPException(status_code=500, detail=f"Failed to create user role: {str(e)}")
    
  


