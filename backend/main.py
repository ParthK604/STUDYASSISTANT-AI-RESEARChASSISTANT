from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.upload import router
from backend.api.query import routerq
from backend.api.messages import router as messages_router


app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.include_router(routerq)
app.include_router(messages_router)

@app.get("/")
async def home():
    return {"message":"hello world"}


