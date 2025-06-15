
from abc import ABC, abstractmethod
from typing import Tuple

from common.decorator import singleton
from handler.handle import FileHandler
from repository.knowledge_base.selector import NewKnowledgeBaseRepository
from repository.file_chunking.selector import NewFileChunkingRepository
from repository.knowledge_base.protocol import KnowledgeBase
from pathlib import Path

class KnowledgeBaseService(ABC):
    @abstractmethod
    def new_knowledge_base(self, name:str, source_dir:str, embedding_opt: str, splitter_opt: str, suffix_list: list[str]) -> Tuple[int, str]:
        pass

    @abstractmethod
    def get_knowledge_base_info_by_id(self,id:int) -> Tuple[Tuple[int, str],str,str]:
       pass

    @abstractmethod
    def get_knowledge_base_info_by_name(self, name:str) -> Tuple[Tuple[int, str],int,str]:
       pass

@singleton
class _KnowledgeBaseServiceImpl(KnowledgeBaseService):

    def __init__(self):
        self.files = Path(__file__).resolve().parent.parent.parent / "files"
        self.knowledge_base_repo = NewKnowledgeBaseRepository()
        self.file_chunking_repo = NewFileChunkingRepository()

    def new_knowledge_base(
            self, name:str, source_dir:str, embedding_opt: str, splitter_opt: str, suffix_list: list[str]
        ) ->  Tuple[int, str]:
        
        sql_result = self.knowledge_base_repo.get_knowledge_base_info_by_name(name)
        if sql_result is not None:
            return 0, f"name {name} is in table knowledge_base"
        
        source_path = Path(source_dir)
        if not source_path.is_dir():
            return 0, f"source_dir {source_dir} is in table knowledge_base"
        
        target_path = self.files / name
        target_path.mkdir(parents=True, exist_ok=True)

        k = KnowledgeBase()
        k.name = name
        k.splitter = splitter_opt
        k.root_dir = str(target_path)
        k.suffix_list = suffix_list
        k.embedding_model = embedding_opt
        knowledge_base_id = self.knowledge_base_repo.new_knowledge_base(k)
        print(f"get knowledge_base_id ${knowledge_base_id}")
        if knowledge_base_id is None:
            return  0, f"new knowledge_base {name} failed"
    
        print(f"handler Init")
        handler = FileHandler(
            knowledge_base_id= knowledge_base_id,
            source_path= source_path,
            target_path= target_path,
            embeddding_opt= embedding_opt,
            splitter_opt= splitter_opt,
            accept_suffix= suffix_list
        )
        print(f"handler Init done")
        handler.spilt_files()
        return knowledge_base_id,""

    def get_knowledge_base_info_by_id(self, id:int) -> Tuple[Tuple[int, str],str,str]:
        Knowledge_base = self.knowledge_base_repo.get_knowledge_base_info_by_id(id)
        if Knowledge_base is None:
            return (), "", f"get knowledge_base info by id:{id} failed"
        
        file_info_list = self.file_chunking_repo.select_files_by_knowledge_base_id(id)
        return file_info_list,Knowledge_base.name ,""

    def get_knowledge_base_info_by_name(self, name:str) -> Tuple[Tuple[int, str],int,str]:
        Knowledge_base = self.knowledge_base_repo.get_knowledge_base_info_by_name(name)
        if Knowledge_base is None:
            return (), "", f"get knowledge_base info by name:{name} failed"
        
        file_info_list = self.file_chunking_repo.select_files_by_knowledge_base_id(Knowledge_base.id)
        return file_info_list,Knowledge_base.name ,""

def NewKnowledgeBaseService() -> KnowledgeBaseService:
    return _KnowledgeBaseServiceImpl()