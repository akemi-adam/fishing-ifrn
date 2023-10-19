from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bagre(Base):
    __tablename__ = "bagres"
    id = Column(String, primary_key=True, index=True)
    specie = Column(String)
    weight = Column(Float)
    size = Column(Integer)
    color = Column(String)
