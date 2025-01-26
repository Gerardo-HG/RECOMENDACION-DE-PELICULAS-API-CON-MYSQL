from pydantic import BaseModel, Field



class RecommenSchema(BaseModel):

    user_id: int = Field(..., description="ID of the user receiving the recommendation")
    movie_id: int = Field(..., description="ID of the movie being recommended")
    method: str = Field(..., description="Method of recommendation")
    description: str = Field(..., min_length=5, max_length=250, description="Description of the recommendation")