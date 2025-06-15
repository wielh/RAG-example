from repository.knowledge_base.protocol import DB as KnowledgeBaseRepository
from repository.knowledge_base.pg_implement import PGRepository

def NewKnowledgeBaseRepository() -> KnowledgeBaseRepository:
    return PGRepository()
