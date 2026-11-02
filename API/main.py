from fastapi import FastAPI
from routers import ia, auth

app = FastAPI()
app.include_router(ia.router)
app.include_router(auth.router)