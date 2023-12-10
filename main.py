import uuid, httpx

from typing import Annotated

from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, Bagre
from validations import BagreEdit, BagreIn, BagreOut, UserCredentials


# Settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Aux functions

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependecies path

async def verify_token(token: Annotated[str, Header()]):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://suap.ifrn.edu.br/api/v2/autenticacao/token/verify/",
            data={"token": token}
        )
    if response.status_code == 401:
        raise HTTPException(
            status_code=401,
            detail='Token inválido ou expirado!'
        )


# Endpoints

@app.post("/login")
async def autenticar_usuario(credentials: UserCredentials):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://suap.ifrn.edu.br/api/v2/autenticacao/token/",
            data={"username": credentials.username, "password": credentials.password}
        )

    if response.status_code == 200:
        return {
            "token": response.json().get('access'),
            "refresh_token": response.json().get('refresh'),
            "status": True
        }
    else:
        raise HTTPException(status_code=response.status_code, detail="Falha na autenticação")
    

@app.post("/bagres", dependencies=[Depends(verify_token)])
def create_bagre(bagre: BagreIn, db=Depends(get_db)):
    bagre_db = Bagre(**bagre.model_dump(), id=str(uuid.uuid4()))
    db.add(bagre_db)
    db.commit()
    db.refresh(bagre_db)
    return BagreOut(**bagre_db.__dict__)


@app.get("/bagres", dependencies=[Depends(verify_token)])
def read_bagres(skip: int = 0, limit: int = 10, db=Depends(get_db)):
    bagres = db.query(Bagre).offset(skip).limit(limit).all()
    return [BagreOut(**bagre.__dict__) for bagre in bagres]


@app.get("/bagres/{uuid}", dependencies=[Depends(verify_token)])
def read_bagre(uuid: str, db=Depends(get_db)):
    bagre = db.query(Bagre).filter(Bagre.id == uuid).first()
    if bagre is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return BagreOut(**bagre.__dict__)


@app.put("/bagres/{uuid}", dependencies=[Depends(verify_token)])
def update_bagre(uuid: str, bagre: BagreEdit, db=Depends(get_db)):
    db_bagre = db.query(Bagre).filter(Bagre.id == uuid).first()
    if db_bagre is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for var, value in bagre.model_dump().items():
        if value is not None:
            setattr(db_bagre, var, value)
    db.add(db_bagre)
    db.commit()
    db.refresh(db_bagre)
    return BagreOut(**db_bagre.__dict__)


@app.delete("/bagres/{uuid}", dependencies=[Depends(verify_token)])
def delete_bagre(uuid: str, db=Depends(get_db)):
    bagre = db.query(Bagre).filter(Bagre.id == uuid).first()
    if bagre is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(bagre)
    db.commit()
    return {"message": "Bagre deleted successfully"}

