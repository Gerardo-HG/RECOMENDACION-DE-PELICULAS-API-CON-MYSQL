from fastapi import APIRouter, HTTPException, Body, Depends
from middlewares.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse
from typing import List
from starlette import status
from schemas.recommendation_schema import RecommenSchema
from config.db import engine
from models.recommendation_model import recommends
from models.user_model import users
from models.movie_model import movies
from sqlalchemy.exc import IntegrityError

recommend_router = APIRouter()

@recommend_router.get(
    path="/api/recommends/{user_id}",
    response_model=List[RecommenSchema],  
    tags=["Recommendations"]
)
def get_recommendation_by_user(user_id: int):
    with engine.connect() as conn:
        try:
            result = conn.execute(recommends.select().where(recommends.c.user_id == user_id)).fetchall()

            if result:
                return {
                    "user_id": result["user_id"],
                    "recommendation": result["recommendation"]
                }
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "Recommendations for this user not found"}
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": f"Could not fetch recommendations: {str(e)}"}
            )


@recommend_router.post(
    path="/api/recommends",
    status_code=status.HTTP_201_CREATED,
    tags=["Recommendations"]
)
def create_recommendation(recommendation_data: RecommenSchema):
    with engine.connect() as conn:
        try:
            users_exits = conn.execute(users.select().where(users.c.user_id == recommendation_data.user_id)).first()
            movies_exits = conn.execute(movies.select().where(movies.c.movie_id == recommendation_data.movie_id)).first()

            if not users_exits:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error" : f"User with id {recommendation_data.user_id} not Found"}
                )

            if not movies_exits:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error" : f"Movie with id {recommendation_data.movie_id} not Found"}
                )
                        
            new_recommendation = recommendation_data.dict()
            conn.execute(recommends.insert().values(new_recommendation))
            conn.commit()

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Recommendation created successfully"}
            )
        
        except IntegrityError as e:
            conn.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Recommendation already exists for this user"}
            )
        
        except Exception as e:
            conn.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": f"Could not create recommendation: {str(e)}"}
            )


@recommend_router.put(
    path="/api/recommends/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=["Recommendations"],
    dependencies=[Depends(JWTBearer())]
)
def update_recommendation(user_id: int, recommendation_data: RecommenSchema):
    with engine.connect() as conn:
        try:
            user_exists = conn.execute(
                users.select().where(users.c.user_id == user_id)
            ).fetchone()

            if not user_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": f"User with id {user_id} not found"}
                )

            movie_exists = conn.execute(
                movies.select().where(movies.c.movie_id == recommendation_data.pelicula_id)
            ).fetchone()

            if not movie_exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": f"Movie with id {recommendation_data.pelicula_id} not found"}
                )

            existing_recommendation = conn.execute(
                recommends.select().where(recommends.c.user_id == user_id)
            ).first()

            if not existing_recommendation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": "Recommendation for this user not found"}
                )

            conn.execute(
                recommends.update()
                .where(recommends.c.user_id == user_id)
                .values(recommendation=recommendation_data.recommendation)
            )
            conn.commit()

            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Recommendation updated successfully"})

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Could not update recommendation"}
            )


@recommend_router.delete(
    path="/api/recommends/{user_id}",
    status_code=status.HTTP_200_OK,
    tags=["Recommendations"],
    dependencies=[Depends(JWTBearer())]
)
def delete_recommendation(user_id: int):
    with engine.connect() as conn:
        try:
            existing_recommendation = conn.execute(
                recommends.select().where(recommends.c.user_id == user_id)
            ).first()

            if not existing_recommendation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error": "Recommendation for this user not found"}
                )

            conn.execute(
                recommends.delete().where(recommends.c.user_id == user_id)
            )
            conn.commit()

            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Recommendation deleted successfully"})

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": "Could not delete recommendation"}
            )