from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    
    file_id: str
    chunk_size: Optional[int] = 100  # Default chunk size 
    overlap_size: Optional[int] = 20  # Default overlap size
    do_reset: Optional[int] = 0  # if you have the same file and want to reset the process, set this to 1
    # do_something => do to indicate that this param will be used to do an action
