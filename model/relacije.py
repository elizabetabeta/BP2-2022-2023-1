from sqlalchemy.orm import relationship

from .breeds import Breed
from .kinds import Kind
from .adoptionApplications import AdoptionApplication
from .pets import Pet
from .users import User
from . import Base
from . import engine

Kind.breeds = relationship("Breed", back_populates="kind")
Breed.kind = relationship("Kind", back_populates="breeds")
AdoptionApplication.pet = relationship("Pet", back_populates="adoptionApplications")
AdoptionApplication.user = relationship("User", back_populates="adoptionApplications") 
Pet.adoptionApplications = relationship("AdoptionApplication", back_populates="pet")
User.adoptionApplications = relationship("AdoptionApplication", back_populates="user")
Pet.breed = relationship("Breed", back_populates="pets")
Breed.pets = relationship("Pet", back_populates="breed")


Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)