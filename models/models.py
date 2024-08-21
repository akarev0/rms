from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from enums import EmployeeLevel, EmployeeEnglishLevel, Position

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class Employee(User):
    __tablename__ = "employees"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    position: Mapped[Position] = mapped_column()
    level: Mapped[EmployeeLevel] = mapped_column()
    english_level: Mapped[EmployeeEnglishLevel] = mapped_column()
    sales_campaign = Column(String)
    other_skills: Mapped[str] = mapped_column()
    team: Mapped["Team"] = relationship("Team", back_populates="employees")
    attendance_link = Column(String)
    last_interview = Column(DateTime)
    skills: Mapped[list["Skill"]] = relationship()


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.user_id"))


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    leader_id = Column(Integer, ForeignKey("users.id"))
    employees: Mapped[list[Employee] | None] = relationship(
        "Employee", back_populates="team"
    )


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="resources")


User.resources = relationship("Resource", back_populates="owner")
