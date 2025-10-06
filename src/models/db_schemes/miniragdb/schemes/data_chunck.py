# ===========================
# DataChunk Model
# ===========================
from models.db_schemes.miniragdb.schemes.miniragdb_base import SQLAlchemyBase 
from sqlalchemy import Column, Integer, DateTime, func, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy import Index
from pydantic import BaseModel
import uuid

class DataChunk(SQLAlchemyBase):
    """
    Represents a text chunk derived from an asset.

    Each `DataChunk` belongs to a specific project and asset. It stores both
    the text content and optional metadata.

    Attributes:
        chunk_id (int): Auto-incremented primary key.
        chunk_uuid (UUID): Unique external identifier for public references.
        chunk_text (str): The text content of the chunk.
        chunk_metadata (dict): Optional metadata stored as JSONB.
        chunk_order (int): Sequence number of the chunk within the source asset.
        chunk_project_id (int): Foreign key to the parent project.
        chunk_asset_id (int): Foreign key to the asset from which this chunk was derived.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
        project (relationship): Reference to the parent `Project`.
        asset (relationship): Reference to the parent `Asset`.
    """

    __tablename__ = "chunks"

    # Primary key and UUID
    chunk_id = Column(Integer, primary_key=True, autoincrement=True)
    chunk_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    # Text data and metadata
    chunk_text = Column(String, nullable=False)
    chunk_metadata = Column(JSONB, nullable=True)  
    chunk_order = Column(Integer, nullable=False)

    # Foreign keys linking to project and asset
    chunk_project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    chunk_asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)

     # Audit timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="chunks")
    asset = relationship("Asset", back_populates="chunks")

    # Indexes to optimize queries by project and asset
    __table_args__ = (
        Index('ix_chunk_project_id', chunk_project_id),
        Index('ix_chunk_asset_id', chunk_asset_id),
    )

class RetrievedDocument(BaseModel):
    """
    Schema representing a retrieved text document (used in retrieval or ranking tasks).

    Attributes:
        text (str): The retrieved text content.
        score (float): The similarity or relevance score.
    """
    text: str
    score: float