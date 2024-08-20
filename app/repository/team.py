from sqlalchemy.orm import Session

from app import schemas
from app.models.models import Team


def create_team(db: Session, team: schemas.TeamCreate):
    db_team = Team(name=team.name, leader_id=team.leader_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
