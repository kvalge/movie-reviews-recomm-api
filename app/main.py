from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, genre

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(genre.router)
