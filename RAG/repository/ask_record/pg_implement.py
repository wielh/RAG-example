
from typing import Any, List, Optional, Tuple
from repository.connection_pool.pg_connection_pool import NewPGConnectPool
from common.decorator import singleton
from repository.ask_record.protocol import DB, EmbeddingSearchRecord
from psycopg2.extras import execute_values

@singleton
class PGRepository(DB):

    def __init__(self):
        self.connection_pool = NewPGConnectPool()
  
    def run_query(self, sql: str, params: tuple | list = (), cursor=None) -> Any:
        if cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
        else:
            conn = self.connection_pool.getconn()
            conn.autocommit = False 
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    result = cur.fetchall()
                    conn.commit()
                    return result
            except Exception as e:
                print(f"[run_query] SQL Error: {e}")
                return None
            finally:
                if conn:
                    self.connection_pool.putconn(conn)

    def insert_batch(self, sql: str, values: List[Tuple], cursor=None):
        if cursor:
            execute_values(cursor, sql, values)
        else:
            conn = self.connection_pool.getconn()
            conn.autocommit = False 
            try:
                with conn.cursor() as cur:
                    execute_values(cur, sql, values)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"[insert_batch] Error: {e}")
            finally:
                self.connection_pool.putconn(conn)
    
    def record_question(self, question:str, knowledge_base_id: int) -> Optional[int]:
        sql = """
            INSERT INTO question_record (question, knowledge_base_id) 
            VALUES (%s, %s) 
            RETURNING id;
        """
        sql_result = self.run_query(sql, (question, knowledge_base_id,))
        if sql_result is None or len(sql_result) == 0:
            return None
        return sql_result[0][0]
    
    def record_question_embedding(self, question_id:int, embedding_model_name:str, embedding: list[float]) -> None:
        embedding_str = '[' + ','.join(str(x) for x in embedding) + ']'
        sql = """
            INSERT INTO question_embedding_record (question_id, embedding_model_name, embedding) VALUES (%s, %s, %s) RETURNING id
        """
        self.run_query(sql, (question_id, embedding_model_name, embedding_str,))

    def record_question_embedding_search(self, question_id:int, records: list[EmbeddingSearchRecord]) -> None:
        sql = """
            INSERT INTO question_search_record (question_id, score, file_id, parent_chunk_index, children_chunk_index) VALUES %s
        """
        values = [
            (
                question_id,
                r.score,
                r.file_id,
                r.parent_chunk_index,
                r.children_chunk_index
            )
            for r in records
        ]
        self.insert_batch(sql, values)

    def record_answer(self, question_id:int, answer: str, llm_model_name: str) -> None:
        sql = """
            INSERT INTO answer_record (question_id, answer, llm_model_name) VALUES (%s, %s, %s) RETURNING id
        """
        self.run_query(sql, (question_id, answer, llm_model_name,))

  