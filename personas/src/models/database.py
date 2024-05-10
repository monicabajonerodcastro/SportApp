from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.services.secret import get_secret
import os

if os.environ["ENVIRONMENT"] == 'prod':
    db_password = "}Zv_2mjr5fRI*IYa"
else:
    db_password = "postgresql"

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(os.environ["DB_USER"], db_password, os.environ["DB_HOST"], os.environ["DB_PORT"], os.environ["DB_NAME"]),
    pool_pre_ping=True
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )
)

Base = declarative_base()