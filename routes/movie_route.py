from fastapi import APIRouter,HTTPException, Body, Depends
from middlewares.jwt_bearer import JWTBearer
from fastapi.responses import JSONResponse
from typing import List
from starlette import status
from schemas.movie_schema import MovieSchema
from config.db import engine
from models.movie_model import movies
from sqlalchemy.exc import IntegrityError

movie_router = APIRouter()

@movie_router.get(
    path="/api/movies",
    response_model=List[MovieSchema],
    status_code=status.HTTP_200_OK,
    tags=["Movie"]
)
def get_all_movies():
    with engine.connect() as conn:
        result = conn.execute(movies.select()).fetchall()

        return result
    

@movie_router.get(
        path="/api/movies/{genero}",
        response_model=List[MovieSchema],
        status_code=status.HTTP_200_OK,
        tags=["Movie"]
)
def get_movies_by_genero(genero : str):
    with engine.connect() as conn:
        try:
            result = conn.execute(movies.select().where(movies.c.genero == genero)).fetchall()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={"error" : f"Movies with {genero} genero not found"}
                )
            
            return result
        
        except Exception as e:
            return 



@movie_router.get(
    path="/api/movies/{movie_id}",
    response_model=MovieSchema,
    status_code=status.HTTP_200_OK,
    tags=["Movie"]
)
def get_movie_by_id(movie_id : int):
    with engine.connect() as conn:
        result = conn.execute(movies.select().where(movies.c.movie_id == movie_id)).first()

        if result:
            return result
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={
                                "message" : "movie not Found"
                            })


@movie_router.post(
    path="/api/movies",
    status_code=status.HTTP_201_CREATED,
    tags=["Movie"]
)
def create_movie(movie_data : MovieSchema = Body(...)):
    with engine.connect() as conn:
        try:
            new_movie = movie_data.dict()

            conn.execute(movies.insert().values(new_movie))
            conn.commit()

            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={
                                    "message" : "movie created successfully"
                                })
    
        except IntegrityError as e:
            conn.rollback()
            if "Duplicate entry" in str(e.orig):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail={"error": "Movie with that title already exists"})
            
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail={"error": "Database error"})
        

@movie_router.put(
    path="/api/movies/{movie_id}",
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Movie"],
    dependencies=[Depends(JWTBearer())]
)
def update_movie(movie_id : int, data_movie : MovieSchema):
    with engine.connect() as conn:
        result = conn.execute(movies.select().where(movies.c.movie_id == movie_id)).first()

        if result:
            conn.execute(movies.update().where(movies.c.movie_id == movie_id).
                            values(title=data_movie.title,
                                    genero=data_movie.genero,
                                    director=data_movie.director,
                                    rating = data_movie.rating,
                                    pub_date=data_movie.pub_date,
                                    decription=data_movie.description))
            
            conn.commit()

            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content={
                                "message":"movie updated successfully"
                            })
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail={
                                "message" : "movie not Found"
                            })
    

@movie_router.delete(
    path="/api/movies/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Movie"],
    dependencies=[Depends(JWTBearer())]
)
def delete_movie(movie_id : int):
    with engine.connect() as conn:
        result = conn.execute(movies.select().where(movies.c.movie_id == movie_id)).first()

        if result:
            conn.execute(movies.delete().where(movies.c.movie_id == movie_id))
            conn.commit()

            return JSONResponse(status_code=status.HTTP_202_ACCEPTED,
                            content={
                                "message":"movie deleted successfully"
                            })

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail={
                                "message" : "movie not Found"
                            })