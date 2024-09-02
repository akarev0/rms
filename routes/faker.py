import random
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from common.enums import EmployeeEnglishLevel, EmployeeLevel, Position
from database.database import get_db
from models.models import Employee, Skill, Team, User
from faker import Faker


fake_router = APIRouter()


@fake_router.get("/generate-fake-data/{limit}")
def read_users(db: Session = Depends(get_db), limit: int = 10):
    fake = Faker()
    try:
        for _ in range(limit):
            team = Team(name=fake.company())
            db.add(team)
            db.flush()  # Flush to get the team ID
            for _ in range(limit):
                user = User(
                    name=fake.name(),
                    email=fake.unique.email(),
                    hashed_password=fake.password(),
                )
                db.add(user)
                db.flush()  # Flush to get the user ID

                employee = Employee(
                    user_id=user.id,
                    name=user.name,
                    email=user.email,
                    position=random.choice(list(Position)),
                    level=random.choice(list(EmployeeLevel)),
                    english_level=random.choice(list(EmployeeEnglishLevel)),
                    sales_campaign=random.choice(list(Position)),
                    other_skills=random.choice(list(Position)),
                    attendance_link=fake.url(),
                    last_interview=fake.date_time_this_year(),
                    team_id=team.id,  # Assuming you have 10 teams
                )
                db.add(employee)
                db.flush()  # Flush to get the employee ID

                # Generate random skills for the employee
                for _ in range(1, 3):
                    skill = Skill(
                        name=random.choice(list(Position)), employee_id=user.id
                    )
                    db.add(skill)

                team.employees.append(employee)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
    return
