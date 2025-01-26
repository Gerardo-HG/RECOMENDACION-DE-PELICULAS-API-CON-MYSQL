from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    
    name : str = Field(..., min_length=4, max_length=30)
    email : EmailStr = Field(..., min_length=4, max_length=30)
    preferences : str = Field(...,min_length=4)


class UserCreate(UserBase):
    password : str = Field(...,min_length=5)

    class Config:
        json_schema_extra = {
            "example" : {
                "name" : "Gerardo",
                "email" : "gerardo123@gmail.com",
                "password" : "12345",
                "preferences": "Accion"
            }
        }


class UserSchema(UserBase):
    pass