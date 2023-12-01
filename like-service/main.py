from fastapi import FastAPI

app = FastAPI()


@app.patch("/like/{page_id}")
async def like(page_id: int):
    return {"message": f"Like page {page_id}!"}