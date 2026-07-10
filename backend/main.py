from fastapi import FastAPI
from backend.api.upload import router
from backend.api.query import routerq


app=FastAPI()
app.include_router(router)
app.include_router(routerq)

@app.get("/")
async def home():
    return {"message":"hello world"}


