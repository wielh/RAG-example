
from abc import ABC, abstractmethod

from repository.ask_record.protocol import EmbeddingSearchRecord
from common.decorator import singleton
from repository.ask_record.selector import NewAskRecordgRepository
from repository.file_chunking.selector import NewFileChunkingRepository
from repository.knowledge_base.selector import NewKnowledgeBaseRepository
from embedding.selector import embedding_selector, EmbeddingModelOption
from llm.selector import llm_selector, LLMModelOption

class AskService(ABC):
    @abstractmethod
    def ask(self, question:str, knowledge_base_id:int) -> str:
        pass

@singleton
class _AskServiceServiceImpl(AskService):
    def __init__(self):
        self.ask_record_repo = NewAskRecordgRepository()
        self.file_chunking_repo = NewFileChunkingRepository()
        self.knowledge_repo = NewKnowledgeBaseRepository()

        # TODO embedding_model 先統一用 all-MiniLM-L6-v2
        self.embedding_model_option = EmbeddingModelOption.MINI_LM
        self.embedding_model = embedding_selector(self.embedding_model_option.value)

        # TODO embedding_model 先統一用 ollama-openchat
        self.llm_model_option = LLMModelOption.OLLAMA_OPENCHAT
        self.llm_model = llm_selector(self.llm_model_option.value)
  
    def ask(self, question:str, knowledge_base_id:int) -> tuple[str, str]:
        knowledge_base_info = self.knowledge_repo.get_knowledge_base_info_by_id(knowledge_base_id)
        if knowledge_base_info is None:
            return "", f"knowledge_base with id:{knowledge_base_id} does not exist"

        question_id = self.ask_record_repo.record_question(question, knowledge_base_id)
        if question_id is None:
            return "", f"ask question failed"
        
        question_vector = self.embedding_model.embedding(question)
        self.ask_record_repo.record_question_embedding(question_id, self.embedding_model_option.value, question_vector)
        print("embedding done")

        fetch_result_list = self.file_chunking_repo.select_top_k_parent_chunk(knowledge_base_id, question_vector, 10, 0.5)
        records = [
            EmbeddingSearchRecord(r.score, r.file_id, r.parent_index, r.children_index) for r in fetch_result_list]
        self.ask_record_repo.record_question_embedding_search(question_id, records)
        print("search done")

        if fetch_result_list is None or len(fetch_result_list) == 0:
            self.ask_record_repo.record_answer(question_id, "找不到相關文檔", self.llm_model_option.value)
            return "", "找不到相關文檔"
        
        docs = [ f.parent_content for f in fetch_result_list ]
        print("search done")
        answer = self.llm_model.ask(question, docs)
        print("回答:", answer)
        self.ask_record_repo.record_answer(question_id, answer, self.llm_model_option.value)
        return answer, ""
    
def NewKnowledgeBaseService() -> AskService:
    return _AskServiceServiceImpl()