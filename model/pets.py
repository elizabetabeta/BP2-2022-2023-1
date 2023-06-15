from . import Base
from sqlalchemy import *


class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    description = Column(String(100))
    breed_id = Column(Integer, ForeignKey("breeds.id"), nullable=True)




