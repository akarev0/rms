from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse

import schemas
from database.database import get_db
from common.enums import EmployeeEnglishLevel, Position
from models.models import Resource, Employee, Team


resource_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@resource_router.get("/resources/", response_model=list[schemas.Resource])
def read_resources(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    resources = db.query(Resource).all()
    return resources


@resource_router.get("/resources/html")
def read_resources_html(
    request: Request, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)
):
    employees = db.query(Employee).offset(skip).all()
    return templates.TemplateResponse(
        "resources.html", {"request": request, "resources": employees}
    )


@resource_router.get("/resources/new")
def new_employee_form(request: Request, db: Session = Depends(get_db)):
    positions = [position.value for position in Position]
    english_levels = [level.value for level in EmployeeEnglishLevel]
    teams = db.query(Team).all()
    return templates.TemplateResponse(
        "new_employee.html",
        {
            "request": request,
            "positions": positions,
            "english_levels": english_levels,
            "teams": teams,
        },
    )


@resource_router.post("/resources/add")
def add_employee(
    name: str = Form(...),
    position: str = Form(...),
    english_level: str = Form(...),
    sales_campaign: str = Form(...),
    other_skills: str = Form(...),
    team_id: str = Form(...),
    attendance_link: str = Form(...),
    last_interview: str = Form(...),
    db: Session = Depends(get_db),
):
    position = Position(position)
    english_level = EmployeeEnglishLevel(english_level)
    team = db.query(Team).filter(Team.id == team_id).first()
    new_employee = Employee(
        name=name,
        position=position,
        english_level=english_level,
        other_skills=other_skills,
        sales_campaign=sales_campaign,
        team=team,
        attendance_link=attendance_link,
        last_interview=last_interview,
    )
    db.add(new_employee)
    db.commit()
    return RedirectResponse(url="/resources/html", status_code=303)


@resource_router.get("/teams/new", response_class=HTMLResponse)
def new_team_form(request: Request):
    team_leaders = ["John Doe", "Jane Doe", "Alice Smith"]
    return templates.TemplateResponse(
        "new_team.html", {"request": request, "team_leaders": team_leaders}
    )


@resource_router.post("/teams/add")
def add_team(
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    new_team = Team(name=name)
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return {"message": "Team created successfully", "team": new_team}
