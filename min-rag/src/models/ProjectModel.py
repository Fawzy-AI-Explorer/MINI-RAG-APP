from src.models.BaseDataModel import BaseDataModel
from src.models.db_schemes.project import Project
from src.models.enums.DataBaseEnums import DataBaseEnum


class ProjectModel(BaseDataModel):

    def __init__(self, db_client:object) -> None:
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
    
    @classmethod
    async def create_instance(cls, db_client:object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()

        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["keys"],
                    name=index["name"],
                    unique=index["unique"]
                )


    async def create_project(self, project:Project):

        # insert_one take a dict {k:v}
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id

        return project
    # ==============================================================
    
    async def get_project_or_create_one(self, project_id:str):

        # find_one return a dict {k:v}
        record = await self.collection.find_one({
            "project_id": project_id # this is a filter (like where in SQL where project_id = project_id)
            })
        if record is None:
            project = Project(project_id=project_id)


            project = await self.create_project(project)

            return project

        return Project(**record) # create a Project object from the dict returned by find_one
    # ==============================================================

    async def get_all_projects(self, page: int=1, page_size: int=10):

        # cout total number of documents in the collection
        total_documents = await self.collection.count_documents({}) # {} means count all documents if you pass filter it will count only those documents that match the filter

        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size) # 
        # documents = list(cursor)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_pages
    # ==============================================================