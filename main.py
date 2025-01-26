#FastAPI
from fastapi import FastAPI


# From Routes
from routes.user_route import user_router
from routes.movie_route import movie_router
from routes.recommend_route import recommend_router
from routes.admin_route import admin_router

# From middlewares
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "API de Recomendacion de Peliculas"

app.add_middleware(ErrorHandler)

app.include_router(user_router)
app.include_router(movie_router)
app.include_router(recommend_router)
app.include_router(admin_router)

@app.get(
    path="/"
)
def home():
    return {"Hello World"}