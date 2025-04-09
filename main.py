from flask import *
from flask_login import login_required, current_user
from .models import *
from datetime import datetime
from . import db
from flask import session
from flask_login import logout_user
main = Blueprint('main', __name__)

@main.route('/')
def index():
    users = User.query.all()
    return render_template('index.html',users=users)

@main.route('/manage')
def manage():
    return render_template('manage.html')

@main.route('/admin')
def admin():
    return render_template('admin.html')


@main.route('/objet')
def objet():
    return render_template('objet.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html') 

@main.route('/delete_profile', methods=['POST'])
@login_required
def delete_profile():
    user = current_user
    
    db.session.delete(user)
    db.session.commit()

    logout_user()

    flash("Votre compte a bien été supprimé.")
    return redirect(url_for('main.index'))

@main.route('/update_profile', methods=['GET', 'POST'])
def edit_user1():
    if request.method == 'POST':
        current_user.email = request.form['email']
        current_user.pseudo = request.form['pseudo']
        current_user.lastname = request.form['lastname']
        current_user.firstname = request.form['firstname']
        current_user.level = request.form['level']
        current_user.age = request.form['age']
        current_user.gender = request.form['gender']
        current_user.role = request.form['role']
        current_user.point = request.form['point']

        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                current_user.image = image_data

        current_user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        db.session.commit()
        return render_template('profile.html')
        

    return render_template('update_profile.html')

@main.route('/search')
def search():
    users = User.query.all()
    objects = Object.query.all()
    rooms = Room.query.all()
    return render_template('search.html', users=users, objects=objects, rooms=rooms)

@main.route('/result')
def result():
    q = request.args.get('q', '')
    service_type = request.args.get('service', '')
    object_type = request.args.get('type', '')
    status = request.args.get('status', '')

    users = User.query.filter(User.pseudo.ilike(f'%{q}%')).all() if service_type in ('', 'Utilisateurs') else []

    objects = Object.query.filter(Object.nom.ilike(f'%{q}%'))
    if object_type:
        objects = objects.filter(Object.type == object_type)
    if status:
        objects = objects.filter(Object.status == status)
    objects = objects.all() if service_type in ('', 'Objets') else []

    rooms = Room.query.filter(Room.nom.ilike(f'%{q}%')).all() if service_type in ('', 'Chambres') else []

    return render_template('search.html', users=users, objects=objects, rooms=rooms)

@main.route('/actualite')
def actualite():
    return redirect(url_for('main.list_actualites'))  # Rediriger vers la page de la liste des actualités

@main.route('/actualites')
def list_actualites():
    actualites = Actualite.query.all()  # Récupérer toutes les actualités
    objets = Object.query.all()  # Récupérer tous les objets existants
    return render_template('actualite.html', actualites=actualites, objets=objets)

@main.route('/add_actualite', methods=['GET', 'POST'])
def add_actualite():
    if request.method == 'POST':
        nom = request.form['nom']
        description = request.form['description']
        image_data = None
        
        # Traitement de l'image téléchargée
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()

        # Création d'une nouvelle actualité
        new_actualite = Actualite(
            nom=nom,
            description=description,
            image=image_data,
            date_creation=datetime.now()
        )

        # Ajout de l'actualité à la base de données
        db.session.add(new_actualite)
        db.session.commit()

        # Redirection vers la page de la liste des actualités
        return redirect(url_for('main.list_actualites'))

    return render_template('add_actualite.html')

@main.route('/delete_actualite/<int:id>', methods=['POST'])
def delete_actualite(id):
    # Récupérer l'actualité à supprimer par son ID
    actualite_to_delete = Actualite.query.get(id)
    
    if actualite_to_delete:
        # Supprimer l'actualité de la base de données
        db.session.delete(actualite_to_delete)
        db.session.commit()

    # Rediriger vers la liste des actualités après la suppression
    return redirect(url_for('main.list_actualites'))


