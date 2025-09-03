# Mi WebService (FastAPI + PostgreSQL @ Render)

## Endpoints
- GET  /api/health
- GET  /api/usuarios
- GET  /api/usuarios/{id}
- POST /api/usuarios
- PUT  /api/usuarios/{id}
- DELETE /api/usuarios/{id}
- Docs: /api/docs

## Variables de entorno
- DATABASE_URL = postgresql+psycopg2://USER:PASS@HOST/DB?sslmode=require

## Run local (opcional)
pip install -r requirements.txt
set DATABASE_URL=postgresql+psycopg2://USER:PASS@HOST/DB?sslmode=require
uvicorn app.main:app --reload --port 8000
