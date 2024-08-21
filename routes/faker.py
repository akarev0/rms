import random
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session


from enums import EmployeeEnglishLevel, EmployeeLevel, Position
from database.database import get_db
from models.models import Employee, Skill, Team, User
from faker import Faker


fake_router = APIRouter()


@fake_router.get("/generate-fake-data/{limit}")
def read_users(db: Session = Depends(get_db), limit: int = 10):
    fake = Faker()
    try:
        # Create 10 teams
        teams = []
        for _ in range(limit):
            team = Team(name=fake.company())
            teams.append(team)
            db.add(team)
        for team in teams:
            users = []
            for _ in range(limit):
                user = User(
                    name=fake.name(),
                    email=fake.unique.email(),
                    hashed_password=fake.password(),
                )
                db.add(user)
                db.flush()
                users.append(user)  # Flush to get the user ID
            for user in users:
                for _ in range(limit):
                    employee = Employee(
                        user_id=user.id,
                        position=random.choice(list(Position)),
                        level=random.choice(list(EmployeeLevel)),
                        english_level=random.choice(list(EmployeeEnglishLevel)),
                        sales_campaign=fake.company(),
                        other_skills=fake.job(),
                        attendance_link=fake.url(),
                        last_interview=fake.date_time_this_year(),
                        team=team,  # Assuming you have 10 teams
                    )
                    db.add(employee)
                    db.flush()  # Flush to get the employee ID

                    # Generate random skills for the employee
                    for _ in range(random.randint(1, 5)):
                        skill = Skill(name=fake.job(), employee_id=employee.user_id)
                        db.add(skill)

        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()
    return
