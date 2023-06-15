from . import Base
from sqlalchemy import *


class Breed(Base):
    __tablename__ = "breeds"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    description = Column(Text)
    kind_id = Column(Integer, ForeignKey("kinds.id"), nullable=True)

