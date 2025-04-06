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
    return render_template('index.html')

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