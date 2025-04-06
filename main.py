from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db
# from .forms import UpdateProfileForm # Pour update_profile
from flask import session
from .ItsDangerous import generate_confirmation_token
from .ItsDangerous import confirm_token
from werkzeug.security import generate_password_hash
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
