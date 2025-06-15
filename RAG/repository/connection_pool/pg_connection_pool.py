from psycopg2 import pool
from psycopg2.pool import AbstractConnectionPool
from common.config import config

pg_config = config["postgres"]
_pg_pool = pool.SimpleConnectionPool(
    minconn=pg_config["minconn"],
    maxconn=pg_config["maxconn"],
    user=pg_config["user"],
    password=pg_config["password"],
    host=pg_config["host"],
    port=pg_config["port"],
    database=pg_config["database"]
)

def NewPGConnectPool() -> AbstractConnectionPool:
    global _pg_pool
    return _pg_pool