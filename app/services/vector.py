from models.vector import Vector
from sqlalchemy.orm import Session

def store_vectors(db: Session, texts: list[str], vectors: list[list[float]], source_name: str):
    for content, embedding in zip(texts, vectors):
        vector = Vector(content=content, embedding=embedding, source=source_name)
        db.add(chunk)
    db.commit()