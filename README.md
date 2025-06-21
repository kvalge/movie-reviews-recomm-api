# Movie Reviews and Recommendations API

## Technologies
Python 3.13.5  
FastAPI  
ASGI server - uvicorn   
Postgres - psycopg2-binary  
ORM - sqlalchemy  
alembic DB migrations  
PyJWT  
passlib[bcrypt] — for secure password hashing  
Docker  

## Setup
pip install fastapi uvicorn psycopg2-binary sqlalchemy alembic PyJWT passlib[bcrypt]  
pip install python-dotenv  

## Run
uvicorn app.main:app --reload  
docker-compose up -d

