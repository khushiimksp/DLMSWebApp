from sqlalchemy import create_all, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from utils.logger import logger

# Create Engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def init_db():
    try:
        # Import models here to ensure they are registered with Base
        import models.meter_master
        import models.instantaneous
        import models.events
        import models.billing
        import models.load_survey
        
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise e

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
