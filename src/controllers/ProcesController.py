from src.controllers.BaseController import BaseController
from src.controllers.ProjectController import ProjectController
# from fastapi import UploadFile
from src.models.enums.ProcessingEnums import ProcessingEnums
# import re
import os
from typing import List
from dataclasses import dataclass
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
# https://python.langchain.com/docs/integrations/document_loaders/

from langchain_text_splitters import RecursiveCharacterTextSplitter # split by characters but not stop in the middle of words if param=10 split by 10 characters if the end of the 10th character is not a space, it will go back to the previous space and split there
# https://python.langchain.com/docs/how_to/recursive_text_splitter/
# https://python.langchain.com/api_reference/text_splitters/character/langchain_text_splitters.character.RecursiveCharacterTextSplitter.html


@dataclass
class Document:
    page_content: str
    metadata: dict

class ProcessController(BaseController):
    
    def __init__(self, project_id: str):
        super().__init__()  # Initialize BaseController to access app settings

        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id) # assets/files/{project_id}

    def get_file_extension(self, file_id: str):
        print(f"file_id : {file_id}")
        
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        
        file_extension = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id) # assets/files/{project_id}/{file_id}

        if not os.path.exists(file_path):
            return None

        if file_extension == ProcessingEnums.PDF.value:
            return PyMuPDFLoader(file_path)
    
        if  file_extension == ProcessingEnums.TXT.value:
            return TextLoader(file_path, encoding="utf8") # encoding to handle special characters and arabic text

        return None
    
    def get_file_content(self, file_id: str):
        
        loader = self.get_file_loader(file_id=file_id)

        if loader:
            documents = loader.load()  
            # List[Document] => Document has page_content and metadata
            # [
            #     Document(page_content='...', metadata={'source': 'path/to/file.pdf', 'page': 0}),
            #     Document(page_content='...', metadata={'source': 'path/to/file.pdf', 'page': 1}),
            # ]

            return documents

        return None

    def process_file_content(self, 
                             file_content: list,
                             file_id: str, 
                             chunk_size: int=100, 
                             overlap_size: int=20):
        

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, # max size of each chunk
            chunk_overlap=overlap_size, # number of overlapping characters between chunks
            length_function=len, # function to measure the length of text to use in split to determine chunk_size is completed  # len() is the default || You can use custom functions if needed (e.g., lambda x: len(x.split())) to split by words instead of characters
        )

        file_content_texts = [
            rec.page_content
            for rec in file_content
        ]

        file_content_metadata = [
            rec.metadata
            for rec in file_content
        ]
        # chunks = text_splitter.create_documents(
        #     file_content_texts,
        #     metadatas=file_content_metadata
        # )
        chunks = self.process_simpler_splitter(
            texts=file_content_texts,
            metadatas=file_content_metadata,
            chunk_size=chunk_size,
            splitter_tag="================"
        )

        return chunks
    
    def process_simpler_splitter(self, 
                                 texts: List[str], 
                                 metadatas: List[dict], 
                                 chunk_size: int, 
                                 splitter_tag: str="================"
        ):
        
        full_text = " ".join(texts)

        # split by splitter_tag
        lines = [ doc.strip() for doc in full_text.split(splitter_tag) if len(doc.strip()) > 0 ]

        # for l in lines:
        #     print(f"line: {l}\n\n")

        chunks = []
        current_chunk = ""

        for line in lines:
            chunks.append(Document(
                page_content=line,
                metadata={}
            ))
        return chunks
        # for line in lines:
        #     current_chunk += line + splitter_tag # remove the splitter_tag if you don't want it in the chunk
        #     if len(current_chunk) >= chunk_size:
        #         chunks.append(Document(
        #             page_content=current_chunk.strip(),
        #             metadata={}
        #         ))

        #         current_chunk = ""

        # if len(current_chunk) >= 0:
        #     chunks.append(Document(
        #         page_content=current_chunk.strip(),
        #         metadata={}
        #     ))

        # return chunks


if __name__ == "__main__":
    print("ProcessController initialized with app settings:")
    controller = ProcessController(project_id="8")
    ext = controller.get_file_extension(r"6rssvl6nmy74_AdhamAllamsCV.pdf")
    print(f"ext : {ext}")

# to run python -m src.controllers.ProcesController