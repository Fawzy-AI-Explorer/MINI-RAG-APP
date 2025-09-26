from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "QDRANT"

class DistanceMetricEnums(Enum):
    COSINE = "Cosine"
    DOT = "Dot"