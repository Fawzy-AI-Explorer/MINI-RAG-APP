from src.models.BaseDataModel import BaseDataModel
from src.models.db_schemes import DataChunk
from bson import ObjectId

from sqlalchemy.future import select
from sqlalchemy import func, delete

class ChunkModel(BaseDataModel):
    """
    Handles operations for DataChunk records.

    The DataChunk model represents text chunks
    extracted from assets, along with metadata and relationships
    to their parent project and asset.
    """

    def __init__(self, db_client: object):
        """
        Initialize the ChunkModel with a database client.

        Args:
            db_client (object): SQLAlchemy async session factory.
        """
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """Create and return an asynchronous instance of ChunkModel."""
        instance = cls(db_client)
        return instance

    async def create_chunk(self, chunk: DataChunk):
        """
        Insert a new chunk record into the database.

        Args:
            chunk (DataChunk): The DataChunk object to insert.

        Returns:
            DataChunk: The inserted chunk object (with updated fields).
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
        return chunk

    async def get_chunk(self, chunk_id: str):
        """
        Retrieve a specific chunk record by its ID.

        Args:
            chunk_id (str): Unique ID of the chunk.

        Returns:
            DataChunk | None: The matching chunk record or None if not found.
        """
        async with self.db_client() as session:
            result = await session.execute(select(DataChunk).where(DataChunk.chunk_id == chunk_id))
            chunk = result.scalar_one_or_none()
        return chunk

    async def insert_many_chunks(self, chunks: list, batch_size: int=100):
        """
        Insert multiple chunk records in batches for performance optimization.

        Args:
            chunks (list): List of DataChunk objects to insert.
            batch_size (int, optional): Batch size for bulk insert. Defaults to 100.

        Returns:
            int: Total number of inserted chunk records.
        """
        async with self.db_client() as session:
            async with session.begin():
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i+batch_size]
                    session.add_all(batch)
            await session.commit()
        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        """
        Delete all chunks belonging to a specific project.

        Args:
            project_id (ObjectId): The project ID whose chunks will be deleted.

        Returns:
            int: Number of deleted rows.
        """
        async with self.db_client() as session:
            stmt = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount
    
    async def get_project_chunks(self, project_id: ObjectId, page_no: int=1, page_size: int=50):
        """
        Retrieve chunks belonging to a specific project.

        Args:
            project_id (ObjectId): Project identifier.
            page_no (int, optional): Page number. Defaults to 1.
            page_size (int, optional): Number of records per page. Defaults to 50.

        Returns:
            list[DataChunk]: List of chunk objects for the given project.
        """
        async with self.db_client() as session:
            stmt = select(DataChunk).where(DataChunk.chunk_project_id == project_id).offset((page_no - 1) * page_size).limit(page_size)
            result = await session.execute(stmt)
            records = result.scalars().all()
        return records
    
    async def get_total_chunks_count(self, project_id: ObjectId):
        """
        Count the total number of chunks for a given project.

        Args:
            project_id (ObjectId): Project identifier.

        Returns:
            int: Total count of chunks associated with the project.
        """
        total_count = 0
        async with self.db_client() as session:
            count_sql = select(func.count(DataChunk.chunk_id)).where(DataChunk.chunk_project_id == project_id)
            records_count = await session.execute(count_sql)
            total_count = records_count.scalar()
        
        return total_count