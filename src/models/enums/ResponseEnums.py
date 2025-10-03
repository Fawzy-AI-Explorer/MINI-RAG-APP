from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATE_SUCCESS = "File validation successful"
    FILE_TYPE_NOT_SUPPORTED = "File type not allowed"
    FILE_SIZE_EXCEEDS_LIMIT = "File size exceeds the maximum limit"
    FILE_UPLOADED_SUCCESSFULLY = "File uploaded successfully"
    FILE_UPLOADED_FAILED = "File upload failed"

    FILE_PROCESSING_FAILED = "File processing failed"
    FILE_PROCESSED_SUCCESSFULLY = "File processed successfully"

    NO_FILE_ERROR = "not_found_files"
    FILE_ID_ERROR = "no_file_found_for_with_this_id"

    PROJECT_NOT_FOUND = "Project with the given ID not found"
    CHUNK_NOT_FOUND = "Data chunk with the given ID not found"

    INSERT_INTO_VECTORDB_ERROR = "Error inserting data into vector database"
    INSERT_INTO_VECTORDB_SUCCESS = "Data inserted into vector database successfully"

    VECTORDB_COLLECTION_RETRIEVED = "Vector database collection information retrieved successfully"
    VECTORDB_SEARCH_ERROR = "Error searching in vector database"
    VECTORDB_SEARCH_SUCCESS = "Search in vector database completed successfully"

    RAG_ANSWER_ERROR = "Error generating answer using RAG"
    RAG_ANSWER_SUCCESS = "Answer generated using RAG successfully"
