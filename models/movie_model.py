from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer,String,Float,Date
from config.db import engine, meta_data

movies = Table("movies",meta_data,
            Column("movie_id",Integer,primary_key=True,autoincrement=True),
            Column("title",String(255),nullable=False,unique=True),
            Column("genero",String(255),nullable=False),
            Column("director",String(255),nullable=False),
            Column("rating",Float,nullable=False),
            Column("pub_date",Date,nullable=False),
            Column("description",String(255),nullable=False)
            )

meta_data.create_all(engine)