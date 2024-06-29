from datetime import datetime, timedelta
from sqlalchemy import Column,Integer,String,DateTime,Boolean,ForeignKey,Table
from project.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String, index=True)
    email=Column(String,unique=True ,index=True)
    phone_number=Column(Integer,unique=True,index=True)
    password=Column(String,index=True)
    otp=Column(String,index=True,nullable=True)
    expires_at=Column(DateTime,nullable=True)
    created_at = Column(DateTime)
    refresh_token = Column(String, nullable=True)
    is_active=Column(Boolean, default=True)
    roles = relationship("UserRole", back_populates="user") 

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship("UserRole", back_populates="role")

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

    # Define relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
