from pydantic import BaseModel
from typing import Optional

class PushRequest(BaseModel):
    do_reset: Optional[int] = 0  # if you have the same file and want to reset(remove all the old), set this to 1

class SearchRequest(BaseModel):
    text: str
    limit: Optional[int] = 5  # number of similar chunks to return

