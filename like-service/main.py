from fastapi import FastAPI, Request
from RedisProxyClient import RedisProxyClient
import psycopg2
from pydantic import BaseModel
from fastapi.responses import JSONResponse


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

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )

@app.post("/page")
def create_page(body: CreatePage):
    cur = pg_conn.cursor()
    cur.execute("INSERT INTO pages (title, body) VALUES (%s, %s) RETURNING id", (body.title, body.body))
    new_page_id = cur.fetchone()[0]

    # insert into Redis
    redis_proxy_client.send_command(f"SET page:{new_page_id}:data {body.title}|{body.body}")

    cur.execute("INSERT INTO likes (page_id, likes_count) VALUES (%s, %s)", (new_page_id, 0))
    pg_conn.commit()
    return {"message": "Page created!"}

@app.patch("/like/{page_id}")
async def like(page_id: int):
    redis_proxy_client.send_command(f"INCR page:{page_id}:likes")
    return {"message": f"Like page {page_id}!"}

@app.get("/pages")
async def get_pages():
    cur = pg_conn.cursor()
    cur.execute("SELECT id FROM pages;")
    page_ids = cur.fetchall()
    pages_json = []

    for page_id in page_ids:
        page_data = redis_proxy_client.send_command(f"GET page:{page_id}:data")
        if page_data:
            title, body = page_data.split('|', 1)
            likes_response = redis_proxy_client.send_command(f"GET page:{page_id}:likes")
            likes_count = int(likes_response) if likes_response else 0

            page_json = {
                "id": page_id,
                "title": title,
                "body": body,
                "likes_count": likes_count
            }
            pages_json.append(page_json)

    return {"pages": pages_json}