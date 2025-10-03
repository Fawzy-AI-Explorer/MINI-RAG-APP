from models.db_schemes import SQLAlchemyBase

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Project(SQLAlchemyBase):

    __tablename__ = "projects" # Refer to table name in the database
    
    project_id = Column(Integer, primary_key=True, autoincrement=True) # this can refer to number of projects in the database so the hacker can guess (number of projects in the database) 
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False) # UUID for public reference it is protected doesn't follow a sequence

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")
