import os
from psycopg2.pool import SimpleConnectionPool

def get_pg_pool():
    # Initialisation
    conn_str = "dbname=deelfietsdashboard"

    if "DB_HOST" in os.environ:
        conn_str += " host={} ".format(os.environ['DB_HOST'])
    if "DB_USER" in os.environ:
        conn_str += " user={}".format(os.environ['DB_USER'])
    if "DB_PASSWORD" in os.environ:
        conn_str += " password={}".format(os.environ['DB_PASSWORD'])
    if "DB_PORT" in os.environ:
        conn_str += " port={}".format(os.environ['DB_PORT'])

    return SimpleConnectionPool(minconn=1, 
            maxconn=10, 
            dsn=conn_str)
