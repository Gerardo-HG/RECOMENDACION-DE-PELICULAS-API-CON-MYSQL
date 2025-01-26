from sqlalchemy import Table, Column, ForeignKey, Enum
from sqlalchemy.sql.sqltypes import Integer,String
from config.db import engine, meta_data
from enum import Enum as PyEnum


class RecommendationMethod(PyEnum):
    collaborative = "collaborative"
    content_based = "content_based"



recommends = Table("recommends", meta_data,
                Column("recommend_id",Integer,primary_key=True,autoincrement=True),
                Column("method", Enum(RecommendationMethod), nullable=False),  
                Column("user_id",Integer,ForeignKey("users.user_id"),unique=True,nullable=False),
                Column("movie_id",Integer,ForeignKey("movies.movie_id"),unique=True,nullable=False),
                Column("description",String(255),nullable=False))
                

meta_data.create_all(engine)