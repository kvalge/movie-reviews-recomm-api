from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user, genre, position, cast_and_crew, country

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Movie Reviews API is running"}

app.include_router(user.router)
app.include_router(genre.router)
app.include_router(position.router)
app.include_router(cast_and_crew.router)
app.include_router(country.router)
