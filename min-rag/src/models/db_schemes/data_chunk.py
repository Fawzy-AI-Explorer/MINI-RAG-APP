from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId


class DataChunk(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    chunck_text: str = Field(..., min_length=1)
    chunck_matadata: dict
    chunck_order: int = Field(..., gt=0)  # Ensure non-negative integer
    chunck_projec_id: ObjectId
    
    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "keys": [("chunck_projec_id", 1)], # 1 for ascending order -1 for descending
                "name": "chunck_projec_id_index_1",
                "unique": False # multiple chunks can belong to the same project
            }
        ]
