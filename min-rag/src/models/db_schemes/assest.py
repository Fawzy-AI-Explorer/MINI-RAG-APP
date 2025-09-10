from pydantic import BaseModel, Field, validator
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):

    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_projec_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config : dict =Field(default=None)
    asset_push_at: datetime=Field(default=datetime.utcnow)
 

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):
        return [
            {
                "keys": [("asset_projec_id", 1)], # 1 for ascending order -1 for descending
                "name": "asset_projec_id_index_1",
                "unique": False # multiple chunks can belong to the same project
            },
            {
                "keys": [
                    ("asset_projec_id", 1), 
                    ("asset_name", 1)
                ],
                "name": "asset_projec_id_name_index_1",
                "unique": True
            }
        ]
