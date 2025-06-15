from abc import ABC, abstractmethod

class FetchResult:
    score: float
    children_content: str
    children_id: int
    children_index: int
    parent_content: str 
    parent_id: int
    parent_index: int
    file_id: int
    file_location: str

class DB(ABC):
    @abstractmethod
    def select_top_k_parent_chunk(self, knowledge_base_id:int, embedding: list[float], k:int, threshold: float) -> list[FetchResult]:
        pass

