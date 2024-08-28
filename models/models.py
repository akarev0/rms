from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from common.enums import EmployeeLevel, EmployeeEnglishLevel, Position

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    employee: Mapped["Employee"] = relationship("Employee", back_populates="user")


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    user: Mapped["User"] = relationship("User", back_populates="employee")
    user_id = Column(Integer, ForeignKey("users.id"))

    position: Mapped[Position] = mapped_column()
    level: Mapped[EmployeeLevel] = mapped_column()
    english_level: Mapped[EmployeeEnglishLevel] = mapped_column()
    sales_campaign = Column(String)
    other_skills: Mapped[str] = mapped_column()
    team_id = Column(Integer, ForeignKey("teams.id"))  # Add team_id as a foreign key
    team: Mapped["Team"] = relationship(
        "Team", back_populates="employees", foreign_keys=[team_id]
    )
    attendance_link = Column(String)
    last_interview = Column(DateTime)
    skills: Mapped[list["Skill"]] = relationship()


class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name: Mapped[str] = mapped_column()
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.user_id"))


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name = Column(String, index=True)
    leader_id = Column(Integer, ForeignKey("users.id"))
    employees: Mapped[list[Employee]] = relationship(
        "Employee", back_populates="team", foreign_keys=[Employee.team_id]
    )


class Resource(Base):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="resources")


User.resources = relationship("Resource", back_populates="owner")
