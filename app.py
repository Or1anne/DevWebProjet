# Importation des bibliothèques
from flask import *
from flask_login import *
from extensions import login_manager

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Nécessaire pour sécuriser les sessions et les cookies

# Initialisation de Flask-Login avec l'application
login_manager.init_app(app)

# Définition des routes de l'application
@app.route("/")
def home():
    """ Route principale : Affiche la page d'accueil """
    return "<p>Page d'accueil</p>"

@app.route("/settings")
@login_required # Protection : Accessible uniquement aux utilisateurs connectés
def settings():
    """ Page des paramètres : Accès restreint aux utilisateurs connectés """
    return "<p>Paramètres</p>"

@app.route("/logout")
@login_required # Protection : Accessible uniquement aux utilisateurs connectés
def logout():
    """ Déconnexion de l'utilisateur et redirection vers l'accueil """
    logout_user() # Déconnection de l'utilisateur
    return redirect(url_for('home')) # Redirection vers la page d'accueil des visiteurs


# Importer les routes APRÈS la création de `app` pour éviter l'import circulaire
if __name__ == '__main__':
    from login import *
    app.run(debug=True)