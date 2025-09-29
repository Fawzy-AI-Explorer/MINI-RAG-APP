from qdrant_client import models, QdrantClient
from src.stores.vectordb.VectorDBInterface import VectorDBInterface
from src.stores.vectordb.VectorDBEnums import DistanceMetricEnums
from src.models.db_schemes.data_chunk import RetrievedDocument
from typing import List
import logging


class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path:str, distance_method: str):

        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMetricEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMetricEnums.DOT.value:
            self.distance_method = models.Distance.DOT


        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(path=self.db_path)

    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str) -> bool:
        if self.is_collection_exists(collection_name):
            return self.client.delete_collection(collection_name=collection_name)


    def create_collection(self, collection_name: str, 
                          embedding_size: int,
                          do_reset: bool = False):

        # print("do reset:", do_reset)
        # if self.is_collection_exists(collection_name):
        #     print("collection existttttttttttttttt")
        # else:
        #     print("collection does not existttttttttttttttt")

        if do_reset:
            _ = self.delete_collection(collection_name = collection_name)

        if not self.is_collection_exists(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size, 
                    distance=self.distance_method
                )
            )
            return True
        return False

    def inser_one(self, collection_name: str, text: str, vector: List, 
                  metadata: dict = None,
                  record_id: str = None):
        
        if not self.is_collection_exists(collection_name):
            self.logger.error(f"cannot insert to non-existing collection: {collection_name}")
            return False
        
        try:
            self.client.upload_points(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=[record_id],
                        payload={
                            "text": text,
                            "metadata": metadata
                        },
                        vector=vector
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"failed to upload point due to {e}")
            return False

        return True


    def insert_many(self, collection_name: str, texts: List, 
                    vectors: List, metadatas: List = None,
                    record_ids: List = None, batch_size: int = 50):
    
        if metadatas is None:
            metadatas = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):

            batch_end = i + batch_size
            batch_texts = texts[i: batch_end]
            batch_vectors = vectors[i: batch_end]
            batch_metadatas = metadatas[i: batch_end]
            batch_record_ids = record_ids[i: batch_end]

            batch_records = [
                models.PointStruct(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x],
                        "metadata": metadatas[x]
                    }
                )
                for x in range(len(batch_texts))
            ]

            try:
                self.client.upload_points(
                collection_name=collection_name,
                points=batch_records
                )
            except Exception as e:
                self.logger.error(f"failed to upload batch starting at index {i} due to {e}")
                return False
        return True


    def search_by_vector(self, collection_name: str, vector: List, 
                         limit: int = 5):
        # if not self.is_collection_exists(collection_name):
        #     self.logger.error(f"cannot search in non-existing collection: {collection_name}")
        #     return None

        # try:
        results =  self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results) == 0:
            return None

        return [
            RetrievedDocument(**{
                "text": result.payload["text"],
                "score": result.score,
            })
            for result in results
        ]
    
