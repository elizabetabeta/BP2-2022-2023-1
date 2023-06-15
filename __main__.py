from model import *
from model.relacije import *
from model.cache import region, api

#docker exec -it redis-stack redis-cli
"""
korisnik = User(name="Pero", lastname="Peric", email="email@email.com", 
                phone_number="123456", user_type="user")
session.add(korisnik)
session.commit()

k = Kind(name="ribica", description="opis")
session.add(k)
session.commit()
"""
kinds = session.query(Kind).all()

for kk in kinds: 
    print(kk.id, kk.name, kk.description)
    #if(ucenik.razred):
    #    print("-",str(ucenik.razred.godina) + " " + ucenik.razred.odjeljenje)

ID = 1
KEY = f'kind_{ID}'
k = region.get(KEY)
print(k)
if k is api.NO_VALUE:
    k = session.query(Kind).filter(Kind.id==ID).one()
    region.set(KEY, k)
print(k.name + " " + k.description)
"""
ID2 = 1
KEY = f'kind_{ID2}'
k = region.get(KEY)
print(k)
if k is api.NO_VALUE:
    k = session.query(Pet).filter(Pet.id==ID2).one()
    region.set(KEY, k)
print(k.name + " " + k.description, k.breed_id)
"""