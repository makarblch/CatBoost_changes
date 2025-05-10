from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = 'model_tasks'
    task_id = Column(String, primary_key=True, index=True)
    status = Column(String, default="running")  # running, done, failed
    model_base64 = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)

# SQLite
engine = create_engine("sqlite:///./models.db")
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
