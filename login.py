# Importation des bibliothèques

from flask import *
from flask_login import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *


# Importation de l'application principale et de la gestion des connexions
from app import app
from extensions import login_manager


# Définition de la vue de connexion par défaut (si un utilisateur non connecté essaie d’accéder à une page protégée)
# TODO : Vérifier si cela est conforme au cahier des charges (CdC)
login_manager.login_view = "login"


# Création du formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) # Champ utilisateur obligatoire
    password = PasswordField('Password', validators=[DataRequired()])  # Champ mot de passe obligatoire
    submit = SubmitField('Login')  # Bouton de soumission du formulaire

# Création d'un utilisateur fictif
class User(UserMixin): # UserMixin permet d'intégrer des fonctionnalités à l'utilisateur
    """ Classe utilisateur simple avec uniquement un identifiant """
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    """ Charge un utilisateur à partir de son identifiant (à remplacer par une vraie requête en base de données) """
    # TODO Remplacer par une vraie recherche en base de données
    return User(user_id)



# Définition de la route pour la connexion des utilisateurs
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit(): # Vérifie si le formulaire est soumis et valide
        # TODO Simuler un utilisateur pour l'exemple (à remplacer par une requête à ta base de données)
        user = User(id=1)  # On crée un utilisateur fictif avec l'ID 1

        login_user(user) # Connecte l'utilisateur
        flash('Connexion réussie') # Affiche un message de succès
        # TODO Changer de redirection car une fois connecté on change de type d'utilisateur 
        # TODO home est la page d'accueil pour les visiteurs donc il faut créer une page pour les simples/complexes/administrateurs
        return redirect(url_for('home'))

    # Si le formulaire n'est pas valide ou si l'utilisateur arrive en GET, on affiche la page de connexion
    return render_template('login.html', form=form)
