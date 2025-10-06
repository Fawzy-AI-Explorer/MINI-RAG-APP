# ===========================
# Asset Model
# ===========================
from models.db_schemes.miniragdb.schemes.miniragdb_base import SQLAlchemyBase 
from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
import uuid

class Asset(SQLAlchemyBase):
    """
    Represents an uploaded file or resource belonging to a project.

    Each `Asset` corresponds to a physical or logical data source (e.g., a PDF, CSV, etc.)
    from which multiple `DataChunk` records may be generated for indexing or analysis.

    Attributes:
        asset_id (int): Auto-incremented internal primary key.
        asset_uuid (UUID): Public unique identifier for secure external access.
        asset_type (str): Type of asset (e.g., "FILE", "TEXT", "URL").
        asset_name (str): Original or generated file name.
        asset_size (int): File size in bytes.
        asset_config (dict): Optional configuration data stored as JSONB.
        asset_project_id (int): Foreign key linking to the parent project.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last modification timestamp.
        project (relationship): Parent `Project` record.
        chunks (relationship): All `DataChunk` records derived from this asset.
    """

    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, autoincrement=True)
    asset_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    asset_type = Column(String, nullable=False)
    asset_name = Column(String, nullable=False)
    asset_size = Column(Integer, nullable=False)
    asset_config = Column(JSONB, nullable=True) # JSONB reduces time for reading JSON data

    asset_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    project = relationship("Project", back_populates="assets")  # get project that this asset belongs to
    chunks = relationship("DataChunk", back_populates="asset")  # get chunks that belong to this asset

    __table_args__ = (  # Index for the foreign key to optimize queries || postgres automatically creates index for primary key and unique (unique=True)
        Index('ix_asset_project_id', asset_project_id),
        Index('ix_asset_type', asset_type),
    )
