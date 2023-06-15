from . import Base
from sqlalchemy import *

class Kind(Base):
    __tablename__ = "kinds"
    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    description = Column(Text)


