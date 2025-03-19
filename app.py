from flask import *
from flask_login import *
from flask_wtf import *
from wtforms import *
from wtforms.validators import *


# Création de l'application Flask
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Nécessaire pour Flask-Login et flash messages

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
# Redirection si non connecté 
# TODO A vérifier si ce n'est pas en conflit avec le CdC
login_manager.login_view = "login" 


# Création du formulaire de connexion
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Création d'un utilisateur fictif
class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    # TODO Remplacer par une vraie recherche en base de données
    return User(user_id)




@app.route("/")
def home():
    return "<p>Page d'accueil</p>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Simuler un utilisateur pour l'exemple (à remplacer par une requête à ta base de données)
        user = User(id=1)  

        login_user(user)
        flash('Connexion réussie')
        return redirect(url_for('home'))

    return render_template('login.html', form=form)



@app.route("/settings")
@login_required
def settings():
    return "<p>Paramètres</p>"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
