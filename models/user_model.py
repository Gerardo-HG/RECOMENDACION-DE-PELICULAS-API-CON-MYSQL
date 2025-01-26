from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer,String
from config.db import engine, meta_data

users = Table("users",meta_data,
            Column("user_id", Integer,primary_key=True, autoincrement=True),
            Column("name", String(255), nullable=False),
            Column("email", String(255),nullable=False,unique=True),
            Column("password",String(255),nullable=False),
            Column("preferences",String(255),nullable=False)
            )

meta_data.create_all(engine)