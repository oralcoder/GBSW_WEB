from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from utils.templates import templates
from core.database import get_db
from schemas.user import UserRegister, UserLogin
from services.user import register_user, authenticate_user

router = APIRouter()

@router.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def process_register(
    request: Request,
    userid: str = Form(...),
    password: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user_data = UserRegister(
        userid=userid,
        password=password,
        name=name,
        email=email
    )
    await register_user(db=db, user_data=user_data)
    return RedirectResponse(url="/", status_code=303)

@router.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def process_login(
    request: Request,
    userid: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user_data = UserLogin(
        userid=userid,
        password=password
    )
    await authenticate_user(db, user_data)
    return RedirectResponse(url="/", status_code=302)
