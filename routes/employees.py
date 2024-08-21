from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from schemas import EmployeeResponseMode
from database.database import get_db
import repository.employees as empl_repo

employee_router = APIRouter()


@employee_router.get("/employees", response_model=list[EmployeeResponseMode])
def get_employees(db: Session = Depends(get_db)):
    return empl_repo.get_employees(db)
