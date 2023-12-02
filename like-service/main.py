from fastapi import FastAPI
from RedisProxyClient import RedisProxyClient
import psycopg2


pg_conn = psycopg2.connect(
    database="likesdb",
    user="likesdb",
    password="likesdb",
    host="postgres-db",
    port=5432
)

app = FastAPI()

redis_proxy_client = RedisProxyClient('localhost', 6379)

@app.post("/page")
def create_page():
    cur = pg_conn.cursor()
    cur.execute("INSERT INTO pages (title, body) VALUES ('My Page', 'This is my page.')")
    pg_conn.commit()
    return {"message": "Page created!"}

@app.patch("/like/{page_id}")
async def like(page_id: int):
    redis_proxy_client.send_command(f"INCR page:{page_id}:likes")
    return {"message": f"Like page {page_id}!"}