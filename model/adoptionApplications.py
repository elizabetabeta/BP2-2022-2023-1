from . import Base
from sqlalchemy import *
import enum

class statusEnum(enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'

class AdoptionApplication(Base):
    __tablename__ = "adoptionApplications"
    id = Column(Integer, primary_key=True)
    application_date = Column(DateTime)
    status = Column(Enum(statusEnum))
    user_id = Column(Integer, ForeignKey("users.id"))
    pet_id = Column(Integer, ForeignKey("pets.id"))




