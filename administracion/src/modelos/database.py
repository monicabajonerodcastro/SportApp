from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.servicios.secret import get_secret
import os

db_password = get_secret(os.environ["PROJECT_ID"], "postgres_password")

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(os.environ["DB_USER"], db_password, os.environ["DB_HOST"], os.environ["DB_PORT"], os.environ["DB_NAME"]),
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()