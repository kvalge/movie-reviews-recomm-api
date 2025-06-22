# Movie Reviews and Recommendations API

## Technologies
Back-end:  
Python 3.13.5  
FastAPI  
ASGI server - uvicorn   
Postgres - psycopg2-binary  
ORM - sqlalchemy  
DB migrations - alembic  
Security - PyJWT  
Password hashing - passlib bcrypt  
Front-end:  
Vue.js  
vite  
Docker  

## Setup
pip install fastapi uvicorn psycopg2-binary sqlalchemy alembic PyJWT passlib[bcrypt]  
pip install pydantic[email]  
pip install python-dotenv  
alembic init alembic  
npm create vite@latest .  
npm install  
npm run dev  


## Run
uvicorn app.main:app --reload  
docker-compose up -d  

## IDE
PyCharm Professional 2025.1.2  

### Migration Generation
alembic revision --autogenerate -m "message"  
alembic upgrade head  



