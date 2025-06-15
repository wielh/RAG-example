from repository.ask_record.protocol import DB as AskRecordRepository
from repository.ask_record.pg_implement import PGRepository

def NewAskRecordgRepository() -> AskRecordRepository:
    return PGRepository()