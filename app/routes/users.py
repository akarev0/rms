from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from app.schemas import UserResponseModel
from app.database.database import get_db
import app.repository.user as user_repo
from app.models.models import User

user_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@user_router.get("/users/", response_model=list[UserResponseModel])
def read_users(db: Session = Depends(get_db)):
    users = user_repo.get_users(db)
    return users


@user_router.get("/users/new", response_class=HTMLResponse)
def new_user_form(request: Request):
    return templates.TemplateResponse("new_user.html", {"request": request})


@user_router.post("/users/add")
def add_user(
    name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/resources/html", status_code=303)
