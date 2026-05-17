import psycopg2
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_connection():
#     try:
#         # For render deployment env variable is defined
#         if DATABASE_URL:
#             conn=psycopg2.connect(DATABASE_URL)
#         else:
#             # local development
#             conn=psycopg2.connect(
#                 host="localhost",
#                 database="student_db",
#                 user="postgres",
#                 password="1805"
#             )
#     except Exception as e:
#         print("Database connection error:",e)
#         return None
