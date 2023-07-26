# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 10:14:12 2023

@author: Anna Shubkina
"""
from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base
import os

host = "127.0.0.1:5432" #insert db IP:port
username = "bot" #insert admin username
password = "MyBotPassword" #insert admin password
database = "tun_tegh" #insert db name

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}/{database}", pool_pre_ping=True)
Base = declarative_base()
variables = MetaData()
MetaData.reflect(variables, bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    name = Column(String)
    surname = Column(String)
    age = Column(String)
    contacts = Column(String)
    referrals = Column(String)
    username = Column(String)
    if_paid = Column(String)

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    ticket_number = Column(String)

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    country = Column(String)

Base.metadata.create_all(engine)
