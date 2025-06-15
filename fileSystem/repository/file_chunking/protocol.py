from abc import ABC, abstractmethod
from typing import Any, Generator, Optional, Tuple



class ParentChunk:
    index: int
    content: str 

class ChildrenChunk:
    index: int
    content: str 
    embedding: list[float]

    def __init__(self, index:int, content:str, embedding: list[float]):
        self.index = index
        self.content = content
        self.embedding = embedding

class DB(ABC):
    @abstractmethod
    def begin_transection(self) -> Generator[Any, Any, Any]:
        pass

    @abstractmethod
    def save_file(self, knowleage_base_id:int, path:str, cursor:Any) -> int:
        pass

    @abstractmethod
    def save_parent_chunk(self, file_id:int, chunk: ParentChunk, cursor:Any) -> int:
        pass

    @abstractmethod
    def save_children_chunks(self, parent_chunk_id:int, chunks: list[ChildrenChunk], cursor:Any) -> None:
        pass

    @abstractmethod
    def select_files_by_knowledge_base_id(self, knowledge_base_id: int) -> list[Tuple[int, str]]:
        pass

    @abstractmethod
    def select_file_by_path(self, path:str) -> Optional[int]:
        pass

    @abstractmethod
    def select_parent_chunks_id_by_file(self, id:int) -> list[int]:
        pass

    @abstractmethod
    def select_child_chunks_id_by_file(self, id:int) -> list[int]:
        pass

    @abstractmethod
    def delete_file(self, file_id: int) -> None:
        pass

    @abstractmethod
    def delete_parent_chunks(self, file_id: int) -> None:
        pass

    @abstractmethod
    def delete_children_chunks(self, parent_chunk_ids: list[int]) -> None:
        pass