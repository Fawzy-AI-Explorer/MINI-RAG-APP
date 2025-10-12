from src.models.BaseDataModel import BaseDataModel
from src.models.db_schemes import Asset
from sqlalchemy.future import select
from sqlalchemy import delete

class AssetModel(BaseDataModel):
    """
    Handles operations for Asset records.

    The Asset model represents uploaded or stored files linked to specific projects,
    including metadata like type, size, and configurations.
    """
    def __init__(self, db_client: object):
        """
        Initialize the AssetModel with a database client.

        Args:
            db_client (object): SQLAlchemy async session factory.
        """
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client: object):
        """Create and return an asynchronous instance of AssetModel."""
        instance = cls(db_client)
        return instance

    async def create_asset(self, asset: Asset):
        """
        Insert a new asset record into the database.

        Args:
            asset (Asset): The Asset ORM object to insert.

        Returns:
            Asset: The inserted asset object.
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(asset)
            await session.commit()
            await session.refresh(asset)
            print(f"Created new asset with ID: {asset.asset_id}")
        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        """
        Retrieve all assets for a specific project and type.

        Args:
            asset_project_id (str): Project identifier.
            asset_type (str): Type of the asset (e.g., 'pdf', 'text', etc.).

        Returns:
            list[Asset]: List of asset records.
        """
        async with self.db_client() as session:
            stmt = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_type == asset_type
            )
            result = await session.execute(stmt)
            records = result.scalars().all()
        return records

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        """
        Retrieve a single asset by its project ID and asset name.

        Args:
            asset_project_id (str): The project ID associated with the asset.
            asset_name (str): The asset name to search for.

        Returns:
            Asset | None: The matching asset or None if not found.
        """
        async with self.db_client() as session:
            stmt = select(Asset).where(
                Asset.asset_project_id == asset_project_id,
                Asset.asset_name == asset_name
            )
            result = await session.execute(stmt)
            record = result.scalar_one_or_none()
        return record
    
    async def delete_assets_by_project_id(self, project_id: str):
        """
        Delete all asset records belonging to a specific project.

        Args:
            project_id (str): The project identifier.

        Returns:
            int: Number of deleted asset records.
        """
        async with self.db_client() as session:
            stmt = delete(Asset).where(Asset.asset_project_id == project_id)
            result = await session.execute(stmt)
            await session.commit()
        return result.rowcount
