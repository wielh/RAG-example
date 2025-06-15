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
    def get_knowledge_base_info_by_id(self,id:int) -> Optional[KnowledgeBase]:
        pass
