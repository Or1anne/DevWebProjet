from flask import *
import base64
from flask_login import login_required, current_user
from .models import *
from . import db
import random
from datetime import datetime

manage_object = Blueprint('manage_object', __name__)


@manage_object.route('/objects')
def list_objects():
    objects = Object.query.all()
    rooms = Room.query.all()
    return render_template('objet.html', objects=objects, rooms=rooms)

@manage_object.route('/add_object', methods=['GET', 'POST'])
def add_object():
    if request.method == 'POST':
        nom = request.form['nom']
        type_obj = request.form['type']
        reference = request.form.get('reference')
        brand = request.form.get('brand')
        status = "OFF"

        battery = random.randint(0,100)
        energy = request.form.get('energy')
        connectivity = request.form.get('connectivity')

        volume = None
        temp = None
        size = None
        resolution = None
        luminosity = None

        if 'size' in request.form:
            size = request.form.get('size', type=int)
            resolution = request.form.get('resolution')

        if 'luminosity' in request.form:
            luminosity = request.form.get('luminosity', type=int)

        if type_obj == "Enceinte" or type_obj == "Television" or type_obj == "Ecran":
            volume = random.randint(0,100)

        if type_obj == "Thermomètre" or type_obj == "Radiateur":
            temp = random.randint(-5,30)

        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()

        new_object = Object(
            nom=nom,
            type=type_obj,
            reference=reference,
            brand=brand,
            status=status,
            image=image_data,
            battery=battery,
            energy=energy,
            connectivity=connectivity
        )

        if size is not None:
            new_object.size = size
            new_object.resolution = resolution

        if volume is not None:
            new_object.volume = volume

        if luminosity is not None:
            new_object.luminosity = luminosity

        if temp is not None:
            new_object.temp = temp

        db.session.add(new_object)
        db.session.commit()
        return redirect(url_for('manage_object.list_objects'))

    return render_template('add_object.html')

@manage_object.route('/profile_object/<int:obj_id>')
def profile_object(obj_id):
    object = Object.query.get(obj_id)
    return render_template('profile_object.html', obj=object)

@manage_object.route('/edit_object/<int:obj_id>', methods=['GET', 'POST'])
def edit_object(obj_id):
    object = Object.query.get(obj_id)
    if not object:
        return "Objet non trouvé", 404
    
    if request.method == 'POST':
        object.nom = request.form['nom']
        object.type = request.form['type']
        object.brand = request.form['brand']
        object.reference= request.form['reference']
        object.battery = request.form['battery']
        object.connectivity = request.form['connectivity']
        object.energy = request.form['energy']

        if object.volume is not None:
            object.volume = request.form['volume']
        if object.temp is not None:
            object.temp = request.form['temp']
        if object.size is not None:
            object.size = request.form['size']
            object.resolution = request.form['resolution']


        db.session.commit()
        return redirect(url_for('manage_object.list_objects'))


    return render_template('edit_profile_object.html', obj=object)

@manage_object.route('/delete_object/<int:obj_id>', methods=['POST'])
def delete_object(obj_id):
    object = Object.query.get(obj_id)
    if object:
        db.session.delete(object)
        db.session.commit()

    return redirect(url_for('manage_object.list_objects'))

@manage_object.route('/activate_object/<int:obj_id>')
def activate_object(obj_id):
    object = Object.query.get(obj_id)
    object.status = "ON"
    db.session.commit()
    return render_template('profile_object.html', obj=object)

@manage_object.route('/desactivate_object/<int:obj_id>')
def desactivate_object(obj_id):
    object = Object.query.get(obj_id)
    object.status = "OFF"
    db.session.commit()
    return render_template('profile_object.html', obj=object)

@manage_object.route('/request_object/<int:obj_id>', methods=['POST'])
def request_object(obj_id):
    title = "Demande de suppression"
    description = request.form.get('description')
    status = "En attente"
    object = Object.query.get(obj_id)
    object_nom = object.nom
    object_type = object.type
    user_lastname = current_user.lastname
    user_firstname = current_user.firstname

    new_request = Request(
            title=title,
            description=description,
            status=status,
            object_name=object_nom,
            object_type=object_type,
            user_lastname=user_lastname,
            user_firstname=user_firstname,
            date=datetime.now()
        )
    
    db.session.add(new_request)
    db.session.commit()
    return redirect(url_for('manage_object.list_objects'))

@manage_object.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        nom = request.form['nom']
        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()

        new_room = Room(
            nom=nom,
            image=image_data
        )

        db.session.add(new_room)
        db.session.commit()
        return redirect(url_for('manage_object.list_objects'))

    return render_template('add_room.html')

@manage_object.route('/profile_room/<int:room_id>')
def profile_room(room_id):
    room = Room.query.get(room_id)
    objects = Object.query.filter_by(room_id=room_id).all()
    return render_template('profile_room.html', room=room, objects=objects)

@manage_object.route('/add_object_room/<int:room_id>/<int:obj_id>', methods=['GET', 'POST'])
def add_object_room(room_id, obj_id):
    from sqlalchemy import or_
    objects = Object.query.filter(Object.room_id == None).all()
    print(objects)
    room = Room.query.get(room_id)
    if obj_id != 0:
        object = Object.query.get(obj_id)
        object.room_id = room_id
        db.session.commit()
        return redirect(url_for('manage_object.list_objects'))
    return render_template('add_object_room.html', objects=objects, room=room)

@manage_object.route('/add_object_room2/<int:room_id>/<int:obj_id>', methods=['GET', 'POST'])
def add_object_room2(room_id, obj_id):
    room = Room.query.all()
    object = Object.query.get(obj_id)
    if room_id != 0:
        object.room_id = room_id
        db.session.commit()
        return redirect(url_for('manage_object.list_objects'))
    return render_template('add_object_room2.html', obj=object, room=room)

@manage_object.route('/remove_object_room/<int:obj_id>', methods=['GET', 'POST'])
def remove_object_room(obj_id):
    object = Object.query.get(obj_id)
    object.room_id = None
    db.session.commit()
    return redirect(url_for('manage_object.list_objects'))

@manage_object.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get(room_id)
    if room:
        objects = Object.query.filter_by(room_id=room_id).all()
        for obj in objects:
            obj.room_id = None
            db.session.commit()
        db.session.delete(room)
        db.session.commit()
    return redirect(url_for('manage_object.list_objects'))

def b64encode_filter(data):
    if data is None:
        return ""
    return base64.b64encode(data).decode('utf-8')