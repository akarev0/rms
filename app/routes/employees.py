from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.schemas import EmployeeResponseMode
from app.database.database import get_db
import app.repository.employees as empl_repo

employee_router = APIRouter()


@employee_router.get("/employees", response_model=list[EmployeeResponseMode])
def get_employees(db: Session = Depends(get_db)):
    return empl_repo.get_employees(db)
