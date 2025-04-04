from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db
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
    user = User.query.get(user_id)  # Récupérer l'utilisateur par son ID
    if not user:
        return "Utilisateur non trouvé", 404

    if request.method == 'POST':
        user.email = request.form['email']
        user.pseudo = request.form['pseudo']
        user.lastname = request.form['lastname']
        user.firstname = request.form['firstname']
        user.level = request.form['level']
        user.age = request.form['age']
        user.gender = request.form['gender']

        db.session.commit()
        return redirect(url_for('admin.gestion_utilisateur'))  # Redirection vers la liste des utilisateurs

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
        user_data = session.get('user_data')
        user = User(
            email=user_data['email'],
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            password=user_data['password'],
            gender=user_data['gender'],
            age=user_data['age'],
            pseudo=user_data['pseudo']
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