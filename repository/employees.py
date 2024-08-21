from sqlalchemy.orm import Session
from models.models import Employee


def get_employees(db: Session) -> list[Employee]:
    return db.query(Employee).all()


def get_employee_by_id(db: Session, user_id: int):
    return db.query(Employee).filter(Employee.id == user_id).first()
