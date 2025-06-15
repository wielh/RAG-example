from abc import ABC, abstractmethod
from typing import Optional

class EmbeddingSearchRecord:
    score: float
    file_id: int
    parent_chunk_index: int
    children_chunk_index: int

    def __init__(self, score, file_id, parent_chunk_index, children_chunk_index):
        self.score = score
        self.file_id = file_id
        self.parent_chunk_index= parent_chunk_index
        self.children_chunk_index= children_chunk_index

class DB(ABC):
    @abstractmethod
    def record_question(self, question:str, knowledge_base_id: int) -> Optional[int]:
        pass
    
    @abstractmethod
    def record_question_embedding(self, question_id:int, embedding_model_name: str, embedding: list[float]) -> None:
        pass

    @abstractmethod
    def record_question_embedding_search(self, question_id:int, records: list[EmbeddingSearchRecord]) -> None:
        pass

    @abstractmethod
    def record_answer(self, question_id:int, answer: str, llm_model_name) -> None:
        pass