# ===========================
# Project Model
# ===========================
from models.db_schemes import SQLAlchemyBase
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

class Project(SQLAlchemyBase):
    """
    Represents a project entity.

    Each project serves as a container for all assets text chunks. 
    A project can have multiple associated `Asset` and `DataChunk` records.

    Attributes:
        project_id (int): Auto-incremented primary key (internal reference).
        project_uuid (UUID): Public unique identifier for secure external reference, it doesn't follow a sequence.
        created_at (datetime): Timestamp of creation (set by the database).
        updated_at (datetime): Timestamp of the last update (automatically updated).
        chunks (relationship): One-to-many relationship to `DataChunk` objects.
        assets (relationship): One-to-many relationship to `Asset` objects.
    """

    __tablename__ = "projects"
    
    # Internal primary key (sequential)
    project_id = Column(Integer, primary_key=True, autoincrement=True) # this can refer to number of projects in the database so the hacker can guess (number of projects in the database)

    # Public UUID (non-sequential, more secure for exposure in APIs)
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    # Audit timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    chunks = relationship("DataChunk", back_populates="project")
    assets = relationship("Asset", back_populates="project")
