from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(os.environ["DB_USER"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_PORT"], os.environ["DB_NAME"]),
)

db_session = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
    )
)

Base = declarative_base()