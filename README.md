# Movie Reviews and Recommendations API

## Technologies

### Backend
- Python 3.13.5  
- FastAPI  
- ASGI server - uvicorn  
- Postgres - psycopg2-binary  
- ORM - SQLAlchemy  
- DB migrations - Alembic  
- Security - PyJWT  
- Password hashing - passlib bcrypt  

### Frontend
- TypeScript  
- JavaScript  
- Vue.js  
- Vite  
- Vue Router  
- Axios  
- Bootstrap  

### Other
- Docker  
- PostgreSQL  

## Backend Dependencies

```bash
pip install fastapi uvicorn psycopg2-binary sqlalchemy alembic PyJWT passlib[bcrypt]
pip install pydantic[email]
pip install python-dotenv
```

## Frontend Dependencies

```bash
npm create vite@latest .
npm install
npm install bootstrap
npm install @popperjs/core
npm install vue-router
npm install axios
```

## Run

```bash
uvicorn app.main:app --reload
docker-compose up -d
npm run dev
```

## Database Migrations

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

## IDE

PyCharm Professional 2025.1.2