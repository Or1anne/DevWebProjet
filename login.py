from flask import *
from flask_login import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Redirection si non connecté 
# TODO A vérifier si ce n'est pas en conflit avec le CdC
login_manager.login_view = "login"