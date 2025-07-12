from sqlalchemy.orm import Session
from sqlalchemy import text

def get_db_version(db: Session) -> str:
    return db.execute(text("SELECT version();")).scalar()
