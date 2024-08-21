from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
import repository.team as team_repo


import schemas
from database.database import get_db
from models.models import Team
from faker import Faker


team_router = APIRouter()


@team_router.get("/teams/", response_model=list[schemas.TeamResponseModel])
def get_teams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    teams = db.query(Team).all()
    return teams


@team_router.post("/teams/", response_model=schemas.TeamResponseModel)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    team = team_repo.create_team(db, team)
    return team


@team_router.post("/teams/add-fake-team", response_model=schemas.TeamResponseModel)
def create_fake_team(db: Session = Depends(get_db)):
    # Initialize Faker
    fake = Faker()
    team = schemas.TeamCreate(name=fake.company(), leader_id=fake.random_int())
    team = team_repo.create_team(db, team)
    return team
