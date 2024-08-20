from sqlalchemy.orm import Session
from app.models.models import Resource, User
from app.models.models import Employee
from app.schemas import ResourceCreate, UserCreate


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        name=user.name, email=user.email, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_resources(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Resource).offset(skip).limit(limit).all()


def create_resource(db: Session, resource: ResourceCreate, user_id: int):
    db_resource = Resource(**resource.dict(), owner_id=user_id)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource
