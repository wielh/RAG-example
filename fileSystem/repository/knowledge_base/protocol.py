from abc import ABC, abstractmethod
from typing import Optional

class KnowledgeBase:
    id: int
    name: str
    splitter: str
    root_dir: str 
    suffix_list: list[str]
    embedding_model: str

class DB(ABC):
    @abstractmethod
    def new_knowledge_base(self,k: KnowledgeBase) -> Optional[int]:
        pass

    @abstractmethod
    def get_knowledge_base_info_by_id(self,id:int) -> Optional[KnowledgeBase]:
        pass

    @abstractmethod
    def get_knowledge_base_info_by_name(self,name:str) -> Optional[KnowledgeBase]:
        pass