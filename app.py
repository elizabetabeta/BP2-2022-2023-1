from model import *
from model.relacije import *
from model.cache import region
from flask import Flask, request, render_template
from flask import jsonify
import json
from kafka import KafkaProducer, KafkaConsumer
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def json_deserializer(data):
    return json.loads(data)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=json_serializer
)

consumer = KafkaConsumer(
    'pet', 'breed', 'kind',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=json_deserializer,
    group_id='test-group',
    auto_offset_reset='earliest'
)

kafka_thread = None


@app.route("/kinds")
def index2 ():
    kinds = session.query(Kind).all()
    return render_template('kinds.html', kinds=kinds)

@app.route("/kinds/delete/<int:id>", methods=["DELETE"])
def delete_kind(id):
    kind = session.query(Kind).get(id)

    if kind:  
        session.delete(kind)
        session.commit()
        return jsonify({'message': f'Kind sa ID {id} je izbrisan.'}), 200
    else:
        return jsonify({'message': f'Nema kinda s ID {id}.'}), 404

@app.route("/kinds/<int:id>", methods=["GET"])
def get_kind(id):
    kind = region.get_or_create(
        f'Kind:{id}', 
        creator=lambda: session.query(Kind).get(id),
        expiration_time=60  
    )
    if kind:
        return jsonify([{"id": kind.id, "name": kind.name, "description": kind.description}]), 200
    else:
        return jsonify({'message': f'Nema vrste s ID {id}.'}), 404

@app.route("/kinds/edit", methods=["PUT"])
def edit_kind():
    id = request.form.get("id")
    name = request.form.get("name")
    description = request.form.get("description")

    if id:  
        kind = session.query(Kind).get(id)
        if kind:  
            if name: 
                kind.name = name
            if description: 
                kind.description = description
            
            session.commit()

            producer.send("kind", [{"id": kind.id, "name": kind.name, "description": kind.description}])
            producer.flush()

            return jsonify({'message': f'Kind sa ID {id} je ažuriran.'}), 200
        else:
            return jsonify({'message': f'Nema kinda s ID {id}.'}), 404
    else:
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/kinds/add", methods=["POST"])
def add_kind():
    name = request.form.get("name")
    description = request.form.get("description")
    
    kind = Kind(name=name, description=description)
    session.add(kind)
    session.commit()

    producer.send("kind", [{"id": kind.id, "name": kind.name, "description": kind.description}])
    producer.flush()

    return jsonify({'message': 'Dodan novi kind u bazu.'})






@app.route("/breeds")
def index3 ():
    breeds = session.query(Breed).all()
    kinds = session.query(Kind).all()
    return render_template('breeds.html', breeds=breeds, kinds=kinds)

@app.route("/breeds/delete/<int:id>", methods=["DELETE"])
def delete_breed(id):
    breed = session.query(Breed).get(id)
    if breed: 
        session.delete(breed)
        session.commit()
        return jsonify({'message': f'Pasmina sa ID {id} je izbrisana.'}), 200
    else:
        return jsonify({'message': f'Nema pasmine s ID {id}.'}), 404

@app.route("/breeds/<int:id>", methods=["GET"])
def get_breed(id):
    breed = region.get_or_create(
        f'Breed:{id}', 
        creator=lambda: session.query(Breed).get(id),
        expiration_time=60 
    )
    if breed:
        return jsonify([{"id": breed.id, "name": breed.name, "description": breed.description, "kind_id": breed.kind_id}]), 200
    else:
        return jsonify({'message': f'Nema pasmine s ID {id}.'}), 404

@app.route("/breeds/edit", methods=["PUT"])
def edit_breed():
    id = request.form.get("id")
    name = request.form.get("name")
    description = request.form.get("description")
    kind_id = request.form.get("kind_id")

    if id:  
        breed = session.query(breed).get(id)
        if breed:  
            if name: 
                breed.name = name
            if description: 
                breed.description = description
            if kind_id: 
                breed.kind_id = kind_id
            
            session.commit()

            producer.send("breed", [{"id": breed.id, "name": breed.name, "description": breed.description, "kind_id": breed.kind.name}])
            producer.flush()

            return jsonify({'message': f'Pasmina sa ID {id} je ažurirana.'}), 200
        else:
            return jsonify({'message': f'Nema pasmine s ID {id}.'}), 404
    else:
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/breeds/add", methods=["POST"])
def add_breed():
    name = request.form.get("name")
    description = request.form.get("description")
    kind_id = request.form.get("kind_id")
    
    breed = Breed(name=name, description=description, kind_id=kind_id)
    session.add(breed)
    session.commit()

    producer.send("breed", [{"id": breed.id, "name": breed.name, "description": breed.description, "kind_id": breed.kind.name}])
    producer.flush()

    return jsonify({'message': 'Dodana nova pasmina u bazu.'})





@app.route("/")
def index ():
    pets = session.query(Pet).all()
    breeds = session.query(Breed).all()
    return render_template('pets.html', pets=pets, breeds=breeds)

@app.route("/pets/delete/<int:id>", methods=["DELETE"])
def delete_pet(id):
    pet = session.query(Pet).get(id)
    if pet: 
        session.delete(pet)
        session.commit()
        return jsonify({'message': f'Ljubimac sa ID {id} je izbrisan.'}), 200
    else:
        return jsonify({'message': f'Nema ljubimca s ID {id}.'}), 404

@app.route("/pets/<int:id>", methods=["GET"])
def get_pet(id):
    pet = region.get_or_create(
        f'Pet:{id}', 
        creator=lambda: session.query(Pet).get(id),
        expiration_time=60 
    )
    if pet:
        return jsonify([{"id": pet.id, "name": pet.name, "description": pet.description, "breed_id": pet.breed_id}]), 200
    else:
        return jsonify({'message': f'Nema ljubimca s ID {id}.'}), 404

@app.route("/pets/edit", methods=["PUT"])
def edit_pet():
    id = request.form.get("id")
    name = request.form.get("name")
    description = request.form.get("description")
    breed_id = request.form.get("breed_id")

    if id:  
        pet = session.query(Pet).get(id)
        if pet:  
            if name: 
                pet.name = name
            if description: 
                pet.description = description
            if breed_id: 
                pet.breed_id = breed_id
            
            session.commit()

            producer.send("pet", [{"id": pet.id, "name": pet.name, "description": pet.description, "breed_id": pet.breed.name}])
            producer.flush()

            return jsonify({'message': f'Ljubimac sa ID {id} je ažuriran.'}), 200
        else:
            return jsonify({'message': f'Nema ljubimca s ID {id}.'}), 404
    else:
        return jsonify({'message': 'ID nije pružen.'}), 400

@app.route("/pets/add", methods=["POST"])
def add_pet():
    name = request.form.get("name")
    description = request.form.get("description")
    breed_id = request.form.get("breed_id")
    
    pet = Pet(name=name, description=description, breed_id=breed_id)
    session.add(pet)
    session.commit()

    producer.send("pet", [{"id": pet.id, "name": pet.name, "description": pet.description, "breed_id": pet.breed.name}])
    producer.flush()

    return jsonify({'message': 'Dodan novi ljubimac u bazu.'})




@socketio.on('connect', namespace='/kafka')
def connect():
    global kafka_thread
    if kafka_thread is None or not kafka_thread.is_alive():
        kafka_thread = threading.Thread(target=kafka_consumer)
        kafka_thread.start()

def kafka_consumer():
    for poruka in consumer:
        pet = poruka.value
        breed = poruka.value
        kind = poruka.value
        socketio.emit('data', {'pet': pet, 'breed': breed, 'kind': kind}, namespace='/kafka')

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, allow_unsafe_werkzeug=True)