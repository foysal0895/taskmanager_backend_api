from sqlalchemy import ForeignKey, Integer, Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    first_name=Column(String(100),nullable=False)
    last_name=Column(String(100),nullable=False)
    email=Column(String(100),nullable=False,unique=True)
    phone=Column(String(20),nullable=False)
    password=Column(String(250),nullable=False)
    created_at=Column(DateTime,nullable=False,default=datetime.datetime.now)
    updated_at=Column(DateTime,nullable=False,default=datetime.datetime.now,onupdate=datetime.datetime.now)


class Task(Base):
    __tablename__="tasks"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String(255),nullable=False)
    description=Column(Text,nullable=True)
    status=Column(String(20),nullable=False,default="new")
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at=Column(DateTime,nullable=False,default=datetime.datetime.now)
    updated_at=Column(DateTime,nullable=False,default=datetime.datetime.now,onupdate=datetime.datetime.now)
