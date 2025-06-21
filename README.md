# Movie Reviews and Recommendations API

## Technologies
Python 3.13.5  
FastAPI — web framework  
uvicorn — ASGI server to run FastAPI  
psycopg2-binary — PostgreSQL driver  
sqlalchemy — ORM  
alembic — for DB migrations  
PyJWT — JWT encoding/decoding  
passlib[bcrypt] — for secure password hashing  

## Set UP
pip install fastapi uvicorn  

## Run
uvicorn app.main:app --reload  
