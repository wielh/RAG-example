from repository.file_chunking.protocol import DB as FileChunkingRepository
from repository.file_chunking.pg_implement import PGRepository

def NewFileChunkingRepository() -> FileChunkingRepository:
    return PGRepository()