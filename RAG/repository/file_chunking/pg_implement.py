
from typing import Any
from repository.connection_pool.pg_connection_pool import NewPGConnectPool
from common.decorator import singleton
from repository.file_chunking.protocol import DB, FetchResult

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

    def select_top_k_parent_chunk(self, knowledge_base_id: int, embedding: list[float], k:int, threshold:float) -> list[FetchResult]:
        sql = """
            SELECT 
                cc.id as children_id, cc.content as children_content, cc.index as children_index, cc.embedding<#> %s AS distance,
                pc.id as parent_id, pc.content as parent_content, pc.index as parent_index, 
                f.id, f.path
            FROM 
                children_chunk cc
            INNER JOIN
                parent_chunk pc ON pc.id = cc.parent_chunk_id
            INNER JOIN
                files f ON f.id=pc.file_id
            WHERE
                f.knowledge_base_id=%s and cc.embedding <#> %s < %s
            ORDER BY 
                distance asc
            LIMIT
                %s
        """
        embedding_str = '[' + ','.join(str(x) for x in embedding) + ']'
        sql_result = self.run_query(sql, (embedding_str, knowledge_base_id, embedding_str, threshold, k))
        result: list[FetchResult] = []
        for row in sql_result:
            r = FetchResult()
            r.children_id = row[0]
            r.children_content = row[1]
            r.children_index = row[2]
            r.score = row[3]
            r.parent_id = row[4]
            r.parent_content = row[5]
            r.parent_index = row[6]
            r.file_id = row[7]
            r.file_location = row[8]
            result.append(r)
        return result
       