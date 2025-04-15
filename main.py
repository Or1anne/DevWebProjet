from flask import *
from flask_login import login_required, current_user, logout_user
from .models import *
from datetime import datetime
from . import db
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

def get_search(q, service_type, object_type, status):

    users = User.query.filter(User.pseudo.ilike(f'%{q}%')).all() if service_type in ('', 'utilisateurs') else []
    rooms = Room.query.filter(Room.nom.ilike(f'%{q}%')).all() if service_type in ('', 'chambres') else []

    objects = Object.query.filter(Object.nom.ilike(f'%{q}%'))
    if object_type:
        objects = objects.filter(Object.type == object_type)
        users = []
        rooms = []
    if status:
        objects = objects.filter(Object.status == status)
        users = []
        rooms = []
    objects = objects.all() if service_type in ('', 'objets') else []

    return users, objects, rooms

@main.route('/')
def index():
    q = request.args.get('q', '')
    service_type = request.args.get('service', '').lower()
    object_type = request.args.get('type', '')
    status = request.args.get('status', '')
    users, objects, rooms = get_search(q, service_type, object_type, status)
    actualites = Actualite.query.order_by(Actualite.date_creation.desc()).limit(2).all()
    return render_template('index.html',users=users, objects=objects, actualites=actualites)

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

        pseudo = request.form['pseudo']
        existing_pseudo = User.query.filter(User.pseudo == pseudo, User.id != current_user.id ).first()
        if existing_pseudo:
            flash("Ce pseudo est déjà utilisé, veuillez en choisir un autre.")
            return redirect(url_for('main.edit_user1'))
        else :
            current_user.pseudo = pseudo
            
        current_user.lastname = request.form['lastname']
        current_user.firstname = request.form['firstname']
        current_user.level = request.form['level']
        current_user.gender = request.form['gender']
        current_user.role = request.form['role']
        current_user.point = request.form['point']
        if current_user.password != request.form['password']:
            current_user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        current_user.birthdate = birthdate

        today = datetime.today()
        current_user.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                current_user.image = image_data

        db.session.commit()
        return render_template('profile.html')
        

    return render_template('update_profile.html')

@main.route('/search')
def search():
    q = request.args.get('q', '')
    service_type = request.args.get('service', '').lower()
    object_type = request.args.get('type', '')
    status = request.args.get('status', '')
    users, objects, rooms = get_search(q, service_type, object_type, status)
    return render_template('search.html', users=users, objects=objects, rooms=rooms)

@main.route('/actualite')
def actualite():
    return redirect(url_for('main.list_actualites'))  # Rediriger vers la page de la liste des actualités

@main.route('/actualite_profile/<int:act_id>')
def actualite_profile(act_id):
    actualite = Actualite.query.get(act_id)
    if current_user.is_authenticated:
        current_user.point += 10
    return render_template("profile_actualite.html", actualite=actualite)

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

@main.route('/request_level/<int:user_id>')
def update_level_request(user_id):

    user = User.query.get(user_id)

    title = "Demande de passage à niveau"
    description = user.firstname + ' ' + user.lastname + " (" + user.pseudo + ")" + " voudrait passer au niveau supérieur."
    status = "En attente"
    if user.level == 'Debutant':
        object_nom = "Debutant -> Intermédiaire"
    elif user.level == 'Intermediaire':
        object_nom = "Intermédiaire -> Avancé"
    elif user.level == 'Avance':
        object_nom = "Avancé -> Expert"
    object_type = user.id
    user_lastname = user.lastname
    user_firstname = user.firstname

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
    flash("Votre demande de passage à niveau a été envoyée avec succès.")
    return redirect(url_for('main.index'))
    