from typing import Any, Optional
from common.decorator import singleton
from repository.connection_pool.pg_connection_pool import NewPGConnectPool
from repository.knowledge_base.protocol import DB, KnowledgeBase

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

    def new_knowledge_base(self, k: KnowledgeBase) -> Optional[int]:
        sql = """
            INSERT INTO knowledge_base (name, splitter, root_dir, suffix_list) 
            VALUES (%s, %s, %s, %s) 
            RETURNING id;
        """
        sql_result = self.run_query(sql, (k.name, k.splitter, k.root_dir, k.suffix_list,))
        if sql_result is None or len(sql_result) == 0:
            return None
        return sql_result[0][0]
    
    def get_knowledge_base_info_by_id(self,id:int) -> Optional[KnowledgeBase]:
        sql = """
        SELECT name, splitter, root_dir, suffix_list, embedding_model FROM knowledge_base WHERE id=%s limit 1
        """

        sql_result = self.run_query(sql, (id,))
        if sql_result is None or len(sql_result) == 0:
            return None
        result = KnowledgeBase()
        result.id = id
        result.name = sql_result[0][0]
        result.splitter = sql_result[0][1]
        result.root_dir = sql_result[0][2]
        result.suffix_list = sql_result[0][3]
        result.embedding_model = sql_result[0][4]
        
    def get_knowledge_base_info_by_name(self,name:str) -> Optional[KnowledgeBase]:
        sql = """
        SELECT name, splitter, root_dir, suffix_list, embedding_model FROM knowledge_base WHERE name=%s limit 1
        """

        sql_result = self.run_query(sql, (name,))
        if sql_result is None or len(sql_result) == 0:
            return None
        result = KnowledgeBase()
        result.id = sql_result[0][0]
        result.name = name
        result.splitter = sql_result[0][1]
        result.root_dir = sql_result[0][2]
        result.suffix_list = sql_result[0][3]
        result.embedding_model = sql_result[0][4]
        
