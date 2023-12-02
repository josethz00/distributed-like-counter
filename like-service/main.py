from fastapi import FastAPI
from RedisProxyClient import RedisProxyClient
import psycopg2
from pydantic import BaseModel


pg_conn = psycopg2.connect(
    database="likesdb",
    user="likesdb",
    password="likesdb",
    host="postgres-db",
    port=5432
)

app = FastAPI()

redis_proxy_client = RedisProxyClient('redis-proxy', 6379)

class CreatePage(BaseModel):
    title: str
    body: str

@app.post("/page")
def create_page(body: CreatePage):
    cur = pg_conn.cursor()
    cur.execute("INSERT INTO pages (title, body) VALUES (%s, %s) RETURNING id", (body.title, body.body))
    new_page_id = cur.fetchone()[0]
    cur.execute("INSERT INTO likes (page_id, likes_count) VALUES (%s, %s)", (new_page_id, 0))
    pg_conn.commit()
    return {"message": "Page created!"}

@app.patch("/like/{page_id}")
async def like(page_id: int):
    redis_proxy_client.send_command(f"INCR page:{page_id}:likes")
    return {"message": f"Like page {page_id}!"}

# mudar para buscar do cache
@app.get("/pages")
async def get_pages():
    cur = pg_conn.cursor()
    cur.execute("SELECT * FROM pages JOIN likes ON pages.id = likes.page_id")
    pages = cur.fetchall()
    pages_json = []

    for page in pages:
        print(page)
        page_json = {
            "id": page[0],
            "title": page[1],
            "body": page[2],
            "likes_count": page[7],
            "created_at": page[3]
        }
        pages_json.append(page_json)

    return {"pages": pages_json}