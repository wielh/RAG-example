
from contextlib import contextmanager
from typing import Any, Generator, List, Optional, Tuple
from common.decorator import singleton
from repository.connection_pool.pg_connection_pool import NewPGConnectPool
from repository.file_chunking.protocol import DB, ParentChunk, ChildrenChunk
from psycopg2.extras import execute_values

@singleton
class PGRepository(DB):

    def __init__(self):
        self.connection_pool = NewPGConnectPool()

    @contextmanager
    def begin_transection(self) -> Generator[Any, Any, Any]:
        conn = self.connection_pool.getconn()
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            yield conn, cursor 
        except Exception as e:
            print(f"[TRANSACTION ERROR] {e}")
            conn.rollback() 
            raise  
        else:
            conn.commit() 
        finally:
            cursor.close()
            self.connection_pool.putconn(conn)

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

    def save_file(self, knowledge_base_id: int, path:str, cursor: Any) -> int:
        sql = """
        INSERT INTO files (knowledge_base_id, path)
        VALUES (%s, %s) 
        RETURNING id;
        """
        sql_result = self.run_query(sql, (knowledge_base_id, path,), cursor=cursor)
        return sql_result[0][0]

    def save_parent_chunk(self, file_id:int, chunk: ParentChunk, cursor: Any) -> int:
        sql = """
        INSERT INTO parent_chunk (file_id, content, index)
        VALUES (%s, %s, %s) 
        RETURNING id;
        """
        sql_result = self.run_query(sql, (file_id, chunk.content, chunk.index,), cursor=cursor)
        return sql_result[0][0]

    def save_children_chunks(self, parent_chunk_id:int, chunks: list[ChildrenChunk], cursor: Any) -> None:
        values = [
            (
                parent_chunk_id,
                chunk.content,
                chunk.embedding,
                chunk.index
            )
            for chunk in chunks
        ]
        sql = """
        INSERT INTO children_chunk (parent_chunk_id, content, embedding, index) VALUES %s;
        """
        self.insert_batch(sql, values, cursor=cursor)

    def select_files_by_knowledge_base_id(self, knowledge_base_id: int) -> list[Tuple[int, str]]:
        sql = """
            SELECT 
                f.id, f.path
            FROM 
                files f 
            WHERE
                f.knowledge_base_id=%s 
        """
        sql_result = self.run_query(sql, (knowledge_base_id,))
        result: list[Tuple[int, str]] = [
            (row[0], row[1], ) for row in sql_result
        ]
        return result

    def select_file_by_path(self, path:str) -> Optional[int]:
        sql = """
            SELECT id
            FROM files
            WHERE path = %s
            LIMIT 1
        """
        sql_result = self.run_query(sql, (path,))
        if sql_result is None or len(sql_result) == 0:
            return None
        return sql_result[0][0]

    def select_parent_chunks_id_by_file(self, file_id:int) -> list[int]:
        sql = """
            SELECT id FROM parent_chunk
            WHERE file_id = %s
            ORDER BY index
        """
        sql_result = self.run_query(sql, (file_id,))
        return [row[0] for row in sql_result]

    def select_child_chunks_id_by_file(self, parent_chunk_id:int) -> list[int]:
        sql = """
            SELECT cc.id
            FROM children_chunk cc
            WHERE cc.parent_chunk_id = %s
            ORDER BY cc.index
        """
        return self.run_query(sql, (parent_chunk_id,))

    def delete_file(self, file_id: int) -> None:
        sql = "DELETE FROM document WHERE id = %s"
        self.run_query(sql, (file_id,))

    def delete_parent_chunks(self, file_id: list[int]) -> None:
        sql = f"DELETE FROM parent_chunk WHERE file_id = %s"
        self.run_query(sql, (file_id,))
        
    def delete_children_chunks(self, parent_chunk_ids: list[int]) -> None:
        if len(parent_chunk_ids) > 0:
            sql = f"DELETE FROM children_chunk WHERE id = ANY(%s)"
            self.run_query(sql, (parent_chunk_ids,))