from src.models.BaseDataModel import BaseDataModel
from src.models.db_schemes import Project
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):
    """
    Handles operations for the Project table in the database.

    This model is responsible for creating, retrieving, and listing project records.
    """

    def __init__(self, db_client:object) -> None:
        """
        Initialize the ProjectModel with a database client.

        Args:
            db_client (object): SQLAlchemy async session factory.
        """
        super().__init__(db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client:object):
        """Create and return an asynchronous instance of ProjectModel."""
        instance = cls(db_client)
        return instance


    async def create_project(self, project:Project):
        """
        Create and insert a new project record into the database.

        Args:
            project (Project): The project object to be inserted.

        Returns:
            Project: The inserted project object (with auto-generated fields refreshed).
        """
        async with self.db_client() as session:
            async with session.begin():
                session.add(project)
            await session.commit()
            await session.refresh(project)
        return project
    
    async def get_project_or_create_one(self, project_id:str):
        """
        Retrieve a project by its ID, or create it if it does not exist.

        Args:
            project_id (str): The ID of the project to retrieve or create.

        Returns:
            Project: The retrieved or newly created project object.
        """
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(Project.project_id == project_id)
                result = await session.execute(query)
                project = result.scalar_one_or_none()
                if project is None:
                    # Create a new project if not found
                    project_record = Project(
                        project_id=project_id
                    )
                    project = await self.create_project(project=project_record)
                    return project
                else:
                    return project

    async def get_all_projects(self, page: int=1, page_size: int=10):
        """
        Retrieve a paginated list of projects.

        Args:
            page (int, optional): The current page number. Defaults to 1.
            page_size (int, optional): The number of records per page. Defaults to 10.

        Returns:
            tuple: A tuple containing:
                - list[Project]: List of project objects.
                - int: Total number of available pages.
        """
        async with await self.db_client() as session:
            async with session.begin():
                # Get total project count
                total_documents = await session.execute(select(
                    func.count(Project.project_id)
                ))
                total_documents = total_documents.scalar_one()

                # Calculate total pages
                total_pages = total_documents // page_size
                if total_documents % page_size > 0:
                    total_pages += 1
                
                query = select(Project).offset((page - 1) * page_size).limit(page_size)
                projects = await session.execute(query).scalars().all()

                return projects, total_pages 

