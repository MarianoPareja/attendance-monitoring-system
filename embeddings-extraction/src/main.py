from fastapi import FastAPI

from endpoints.embeddings import emb_router

app = FastAPI()
app.include_router(emb_router)


@app.get("/")
async def root():
    return {"testing": "testing"}
