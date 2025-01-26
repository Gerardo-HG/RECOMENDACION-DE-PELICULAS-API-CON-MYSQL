from pydantic import BaseModel, Field
from datetime import date

class MovieSchema(BaseModel):

    title : str = Field(..., min_length=5,max_length=20)
    genero : str = Field(..., min_length=5, max_length=15)
    director : str = Field(..., min_length=6, max_length=25)
    rating : float = Field(..., gt=0)
    pub_date : date = Field(...)
    description : str = Field(..., min_length=8)
