from enum import Enum

class LLMEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAIEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CoHereEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "CHATBOT"

    DOCUMENT = "search_document" # DOC : document you want to search within
    QUERY = "search_query"       # Query : the Question


class DocumentTypeEnums(Enum):
    DOCUMENT = "document"
    QUERY = "query"