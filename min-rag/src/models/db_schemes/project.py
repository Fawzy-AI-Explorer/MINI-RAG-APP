from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId


class Project(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)


    @validator("project_id")
    def validate_object_id(cls, value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value
    
    class Config: # to validate non pydantic types like ObjectId
        arbitrary_types_allowed = True
