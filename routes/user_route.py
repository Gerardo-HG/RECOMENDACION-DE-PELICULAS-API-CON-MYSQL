from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import Body, Depends
from typing import List
from starlette import status
from werkzeug.security import generate_password_hash
from schemas.user_schema import UserCreate, UserSchema
from config.db import engine
from models.user_model import users
from sqlalchemy.exc import IntegrityError
from middlewares.jwt_bearer import JWTBearer

user_router = APIRouter()

@user_router.get(
    path="/api/users",
    response_model=List[UserSchema],
    status_code=status.HTTP_200_OK,
    tags=["User"]
)
def get_all_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()

        users_list = [dict(row) for row in result]
        return users_list


@user_router.get(
    path="/api/users/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    tags=["User"]
)
def get_user_by_id(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.user_id == user_id)).first()

        if result:
            return dict(result)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                "message" : "User not found"
            })


@user_router.post(
    path="/api/users",
    status_code=status.HTTP_201_CREATED,
    tags=["User"]
)
def create_user(user_data: UserCreate = Body(..., description="Creating a user")):
    with engine.connect() as conn:
        try:
            new_user = user_data.dict()
            new_user["password"] = generate_password_hash(user_data.password, "pbkdf2:sha256:30")

            conn.execute(users.insert().values(new_user))
            conn.commit()

            return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={
                                "message" : "User created successfully",
                                "user": new_user
                            })

        except IntegrityError as e:
            conn.rollback()
            if "Duplicate entry" in str(e.orig):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={"error": "Email already exists"})
            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={"error": "Database error"})


@user_router.put(
    path="/api/users/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["User"],
    dependencies=[Depends(JWTBearer())]
)
def update_user(user_id: int, data_user: UserCreate):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.user_id == user_id)).first()

        if result:
            encrypt_password = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)
            conn.execute(users.update().where(users.c.user_id == user_id).
                                        values(name=data_user.name,
                                               password=encrypt_password,
                                               preferences=data_user.preferences))

            conn.commit()

            updated_user = conn.execute(users.select().where(users.c.user_id == user_id)).first()
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content={
                                "message": "User updated successfully",
                                "user": dict(updated_user)
                            })
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail={
                                "message" : "User not found"
                            })


@user_router.delete(
    path="/api/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["User"],
    dependencies=[Depends(JWTBearer())]
)
def delete_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.user_id == user_id)).first()

        if result:
            conn.execute(users.delete().where(users.c.user_id == user_id))
            conn.commit()
            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content={
                                "message": "User deleted successfully"
                            })

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail={
                                "message" : "User not found"
                            })
