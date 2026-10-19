from fastapi import FastAPI
from routers import ia

app = FastAPI()
app.include_router(ia.router)