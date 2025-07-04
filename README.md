# Movie Reviews and Recommendations API

## Implemented functionalities
User Registration – create a new user account.  
User Login & Logout – secure authentication flow with session/token support.  
Authentication Handling – protect routes and resources based on login status.  
Add, edit, delete genre, position (role of the crew members).  

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
- Pinia  
- Bootstrap  
- CSS  


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
npm install pinia
```

## Run

```bash
# uvicorn app.main:app --reload
docker-compose build
docker-compose up -d
npm run dev
```

## Testing

### Backend Tests
From root directory:
```bash
pytest
```

### Frontend Tests
From root directory:
```bash
cd vue-app; npm test
```

```bash
cd vue-app; npm run test:e2e
```
*(requires dev server running)*

## Database Migrations

### Quick Migration Commands

**Windows (PowerShell):**
```powershell
# Generate and apply migration for new models
.\migrate.ps1 full-migrate "Initial schema."

# Apply pending migrations only
.\migrate.ps1 apply

# Rebuild containers after code changes
.\migrate.ps1 rebuild

# Check migration status
.\migrate.ps1 status
```

**Linux/Mac:**
```bash
# Generate and apply migration for new models
./migrate.sh full-migrate "add genres table"

# Apply pending migrations only
./migrate.sh apply

# Rebuild containers after code changes
./migrate.sh rebuild

# Check migration status
./migrate.sh status
```

### Manual Migration Commands

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head

alembic revision --autogenerate -m "message"
docker-compose build
```

## IDE
PyCharm Professional 2025.1.2

## Swagger
http://127.0.0.1:8000/docs
