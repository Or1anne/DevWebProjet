from flask import *
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import *
from .models import *
from . import db, mail
from .ItsDangerous import generate_confirmation_token, confirm_token
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login2.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

#Inscription de l'utilisateur + envoi d'un mail de confirmation
@auth.route('/signup', methods=['POST'])
def signup_post():

    email=request.form.get('email')
    pseudo=request.form.get('pseudo')
    password=generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    gender=request.form.get('gender')
    birthdate=datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d')
    
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    user_by_email = User.query.filter_by(email=email).first()
    user_by_pseudo = User.query.filter_by(pseudo=pseudo).first()

    if user_by_email:  # Vérifie si l'email existe déjà
        flash('Cet email est déjà utilisé.')
        return redirect(url_for('auth.signup'))

    if user_by_pseudo:  # Vérifie si le pseudo existe déjà
        flash('Ce pseudo est déjà utilisé.')
        return redirect(url_for('auth.signup'))
    
    session['user_data'] = {
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'password': password,
        'age' : age,
        'gender' : gender,
        'pseudo' : pseudo,
        'birthdate' : birthdate,
        'confirmed' : False
    }
    
    token = generate_confirmation_token(email)
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)

    msg = Message('Confirmez votre email', recipients=[email])
    msg.body = f'Bonjour {firstname} {lastname}, \n \nMerci de vous être inscrit, veuillez cliquer sur lien pour confirmer votre adresse mail : {confirm_url}'
    try:
        mail.send(msg)
        flash("Veuillez vérifier votre email pour confirmer votre inscription.")
    except Exception as e:
        return redirect(url_for('auth.signup'))

    return redirect(url_for('main.index'))

#Vérification du token de confirmation d'email
@auth.route('/confirm/<token>')
def confirm_email(token):

    email = confirm_token(token)
    if not email:
        return redirect(url_for('auth.signup'))
    
    user_data = session.get('user_data')
    if user_data['confirmed']:
        flash("Votre email a déjà été confirmé.", "info")
        return redirect(url_for('main.index'))
    user_data['confirmed'] = True
    
    new_request = Request(
        title = "Demande d'inscription",
        description = user_data['firstname'] + " " + user_data['lastname'] + " a demandé à s'inscrire.",
        status = "En attente",
        user_lastname = user_data['lastname'],
        user_firstname = user_data['firstname'],
        date=datetime.now()
    )

    db.session.add(new_request)
    db.session.commit()

    flash("Votre inscription a bien été envoyée, en attente de validation par l'amdinistrateur.")
    return redirect(url_for('main.index'))

#Connexion de l'utilisateur
@auth.route('/login', methods=['POST'])
def login_post():
    pseudo = request.form.get('pseudo')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(pseudo=pseudo).first()

    if not user or not check_password_hash(user.password, password):
        flash('Identifiant ou mot de passe incorrect, veuillez réessayer.')
        return redirect(url_for('auth.login'))
    else:
        login_user(user, remember=remember)
        user.point += 10
        db.session.commit()
        return redirect(url_for('main.index'))

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))