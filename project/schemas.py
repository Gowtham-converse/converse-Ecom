from pydantic import BaseModel, EmailStr, validator,Field
from typing import Optional


class User(BaseModel):
    name: str
    email: EmailStr
    phone_number: int
    password: str

    @validator('*', pre=True, always=True)
    def field_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('This field should not be empty')
        return value


class UserCreate(BaseModel):
    otp: str


class UserSingle(User):
    id: int

    class Config:
        from_attributes = True


class User_role(User):
    roles: str

    @validator('roles', pre=True, always=True)
    def field_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('This field should not be empty')
        return value


class ResetEmail(BaseModel):
    email: EmailStr


class ResetOtp(BaseModel):
    otp: str


class ResetPassword(BaseModel):
    NewPassword: str
    ConfirmPassword: str


class Role(BaseModel):
    name: str

    class Config:
        from_attributes = True

class UpdateRoleNameRequest(BaseModel):
    new_name: str

class UpdateUserSchema(BaseModel):
    name: str
    password: str
    roles: str

    @validator('name', 'password', 'roles', pre=True, always=True)
    def field_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('This field should not be empty')
        return value
    
#copy
class user(BaseModel):
      email:str
      password:str

class User_LoginBase(BaseModel):
      email_or_phonenumber:str
class User_Login(User_LoginBase):
      password:str=Field(...)

class OTP(BaseModel):
      Otp:str

class change_password(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class refresh_Token(BaseModel):
      refresh_token:str

#copy