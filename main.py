from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Float, Integer
import uuid

from models import Base, Bagre

app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing) to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the database connection
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BagreIn(BaseModel):
    specie: str
    weight: float
    size: int
    color: str


class BagreOut(BaseModel):
    id: str
    specie: str
    weight: float
    size: int
    color: str


@app.post("/bagres/")
def create_bagre(bagre: BagreIn, db=Depends(get_db)):
    bagre_db = Bagre(**bagre.dict(), id=str(uuid.uuid4()))
    db.add(bagre_db)
    db.commit()
    db.refresh(bagre_db)
    return BagreOut(**bagre_db.__dict__)


@app.get("/bagres/")
def read_bagres(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    bagres = db.query(Bagre).offset(skip).limit(limit).all()
    return [BagreOut(**bagre.__dict__) for bagre in bagres]


@app.get("/bagres/{uuid}")
def read_bagre(uuid: str, db=Depends(get_db)):
    bagre = db.query(Bagre).filter(Bagre.id == uuid).first()
    if bagre is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return BagreOut(**bagre.__dict__)


@app.put("/bagres/{uuid}")
def update_bagre(uuid: str, bagre: BagreIn, db=Depends(get_db)):
    db_bagre = db.query(Bagre).filter(Bagre.id == uuid).first()
    if db_bagre is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in bagre.dict().items():
        if value is not None:
            setattr(db_bagre, var, value)
    db.add(db_bagre)
    db.commit()
    db.refresh(db_bagre)
    return BagreOut(**db_bagre.__dict__)


@app.delete("/bagres/{uuid}")
def delete_bagre(uuid: str, db=Depends(get_db)):
    bagre = db.query(Bagre).filter(Bagre.id == uuid).first()
    if bagre is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(bagre)
    db.commit()
    return {"message": "Bagre deleted successfully"}

