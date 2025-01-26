from pydantic import BaseModel


class Admin(BaseModel):
    email:str
    password:str

    class Config:
        json_schema_extra = {
            "example" : {
                "email" : "admin@gmail.com",
                "password" : "admin"
            }
        }