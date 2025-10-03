from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "QDRANT"
    PGVECTOR = "PGVECTOR"

class DistanceMethodEnums(Enum):
    COSINE = "Cosine"
    DOT = "Dot"

class PgVectorTableSchemeEnums(Enum):
    ID = 'id'    
    TEXT = 'text' # this for debugging purposes only
    VECTOR = 'vector'
    CHUNK_ID = 'chunk_id'  # foreign key to chunks table
    METADATA = 'metadata'
    _PREFIX = 'pgvector' # will be exist in the start of the PGVector Tables (there is no direct way to get all tables with vector type) wee will use this prefix to identify them

class PgVectorDistanceMethodEnums(Enum):
    COSINE = "vector_cosine_ops"
    DOT = "vector_l2_ops"

class PgVectorIndexTypeEnums(Enum):
    # if you have 100 chunks => 100 Embedding || Qustion >> Embedding => search on 100 Embeddings || 
    # when you have 1M chunks =>  VERY SLOW

    HNSW = "hnsw" # this cluster similar vectors together and search within those clusters (Centroids)
    IVFFLAT = "ivfflat"  #
