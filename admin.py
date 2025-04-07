from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db
from datetime import datetime
from flask import session

admin = Blueprint('admin', __name__)

#pour la gestion
@admin.route('/gestion')
def gestion_utilisateur():
    users = User.query.all()
    return render_template('admin_gestion_utilisateur.html', users=users)

@admin.route('/userProfile/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('admin_user_profile.html', user=user)

@admin.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    
    user = User.query.get(user_id)

    if request.method == 'POST':
        user.email = request.form['email']
        user.pseudo = request.form['pseudo']
        user.lastname = request.form['lastname']
        user.firstname = request.form['firstname']
        user.level = request.form['level']
        user.age = request.form['age']
        user.gender = request.form['gender']
        user.role = request.form['role']
        user.point = request.form['point']

        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                user.image = image_data

        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()

        db.session.commit()
        return redirect(url_for('admin.gestion_utilisateur'))

    return render_template('admin_edit_user.html', user=user)

@admin.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('admin.gestion_utilisateur'))

#Requêtes d'admin
@admin.route('/request_admin')
def request_admin_list():
    requests = Request.query.all()
    return render_template('admin_request.html', requests=requests)

@admin.route('/accept/<int:request_id>', methods=['POST'])
def request_accept(request_id):
    request = Request.query.get(request_id)
    if request.title == "Demande de suppression":
        request.status = "Acceptée"
        object = Object.query.filter_by(nom=request.object_name).first()
        db.session.delete(object)
        db.session.commit()
    elif request.title == "Demande d'inscription":
        #TODO Attribuer un rôle à l'utilisateur
        user_data = session.get('user_data')
        user = User(
            email=user_data['email'],
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            password=user_data['password'],
            gender=user_data['gender'],
            age=user_data['age'],
            pseudo=user_data['pseudo'],
            birthdate = datetime.strptime(user_data['birthdate'], '%Y-%m-%d').date()
        )
        request.status = "Acceptée"
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('admin.request_admin_list'))

@admin.route('/refuse/<int:request_id>', methods=['POST'])
def request_refuse(request_id):
    request = Request.query.get(request_id)
    if request.title == "Demande de suppression":
        request.status = "Refusée"
        db.session.commit()
    elif request.title == "Demande d'inscription":
        session.pop('user_data', None)
        request.status = "Refusée"
        db.session.commit()
    return redirect(url_for('admin.request_admin_list'))