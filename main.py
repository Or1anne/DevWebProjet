from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/manage')
def manage():
    return render_template('manage.html')

@main.route('/admin')
def admin():
    return render_template('admin.html')

@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.firstname)

@main.route('/update_profile')
def update_profile():
    return render_template('update_profile.html', name=current_user.firstname)

#pour la gestion
@main.route('/gestion')
def gestion_utilisateur():
    users = User.query.all()
    return render_template('gestion_utilisateur.html', users=users)

@main.route('/userProfile/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('user_profile.html', user=user)

@main.route('/edit/<int:user_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('main.gestion_utilisateur'))  # Redirection vers la liste des utilisateurs

    return render_template('edit_user.html', user=user)

@main.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('main.gestion_utilisateur'))

