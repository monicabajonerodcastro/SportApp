from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.utilidades import utilidades_gcp
import os

postgres_password = utilidades_gcp.obtener_secreto(os.environ["PROJECT_ID"], os.environ["SECRET_PASSWORD_DB_ID"])

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(os.environ["DB_USER"], postgres_password, os.environ["DB_HOST"], os.environ["DB_PORT"], os.environ["DB_NAME"]),
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()