from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, 
    poolclass=NullPool,  # <-- evita mantener la conexión abierta
    pool_pre_ping=True)

# Crea sesiones nuevas por request (modo sincrónico)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
