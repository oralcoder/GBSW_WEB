from core.database import Base, engine
from models import user, vector

def create_tables():
    Base.metadata.create_all(bind=engine)