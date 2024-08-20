import random
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Base, User, Employee, Skill, Team
from app.enums import EmployeeLevel, EmployeeEnglishLevel, Position
from app.database.database import DATABASE_URL

# Initialize Faker
fake = Faker()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Generate random employees
def generate_employees(n=10):
    session = SessionLocal()
    try:
        # Create 10 teams
        teams = []
        for _ in range(n):
            team = Team(name=fake.company())
            teams.append(team)
            session.add(team)
        for team in teams:
            for _ in range(n):
                user = User(
                    name=fake.name(),
                    email=fake.unique.email(),
                    hashed_password=fake.password(),
                )
                session.add(user)
                session.flush()  # Flush to get the user ID

                employee = Employee(
                    id=user.id,
                    position=random.choice(list(Position)),
                    level=random.choice(list(EmployeeLevel)),
                    english_level=random.choice(list(EmployeeEnglishLevel)),
                    sales_campaign=fake.company(),
                    other_skills=fake.job(),
                    attendance_link=fake.url(),
                    last_interview=fake.date_time_this_year(),
                    team=team,  # Assuming you have 10 teams
                )
                session.add(employee)

                # Generate random skills for the employee
                for _ in range(random.randint(1, 5)):
                    skill = Skill(name=fake.job(), employee_id=employee.id)
                    session.add(skill)

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    generate_employees()
