from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

user = os.environ.get("MYSQL_USER")
hostname = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
password = os.environ.get("MYSQL_ROOT_PASSWORD")
db = os.environ.get("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://root:{password}@{hostname}:{port}/{db}" 
print(DATABASE_URL)

engine = create_engine(DATABASE_URL, pool_size=200, max_overflow=250)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to get a SQLAlchemy DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
