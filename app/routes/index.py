from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from core.database import get_db
from utils.templates import templates
from services.version import get_db_version

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    version = get_db_version(db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Hello from host → container",
        "db_version": version
    })
