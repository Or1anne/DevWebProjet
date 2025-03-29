from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db
from .forms import UpdateProfileForm # Pour update_profile
from flask import session
from .ItsDangerous import generate_confirmation_token
from .ItsDangerous import confirm_token

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
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user) 

@main.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # Vérifie domaine email
        if not form.email.data.endswith('@etu.cyu.fr'):
            flash("❗️ Veuillez utiliser une adresse email valide au format : prenom.nom@etu.cyu.fr")
            return redirect(url_for('main.update_profile'))

        # Vérifie si le pseudo est déjà utilisé par un autre utilisateur
        existing_pseudo = User.query.filter_by(pseudo=form.pseudo.data).first()
        if existing_pseudo and existing_pseudo.id != current_user.id:
            flash("❗️ Ce pseudo est déjà utilisé. Veuillez en choisir un autre.")
            return redirect(url_for('main.update_profile'))

        # Si l'utilisateur change son email → Confirmation par mail
        if form.email.data != current_user.email:
            session['update_data'] = {
                'firstname': form.firstname.data,
                'lastname': form.lastname.data,
                'age': form.age.data,
                'gender': form.gender.data,
                'email': form.email.data,
                'pseudo': form.pseudo.data
            }

            token = generate_confirmation_token(form.email.data)
            confirm_url = url_for('main.confirm_update_email', token=token, _external=True)

            from . import mail
            from flask_mail import Message

            msg = Message('Confirmez la modification de votre email', recipients=[form.email.data])
            msg.body = f'Bonjour {current_user.firstname},\n\nVeuillez cliquer sur le lien suivant pour confirmer votre nouvelle adresse email : {confirm_url}'

            try:
                mail.send(msg)
            except Exception as e:
                flash('Erreur lors de l’envoi de l’email de confirmation.')
                return redirect(url_for('main.update_profile'))

            flash('Un email de confirmation a été envoyé à votre nouvelle adresse. Veuillez confirmer.')
            return redirect(url_for('main.profile'))

        # Si l'email ne change pas → Mise à jour directe
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.pseudo = form.pseudo.data

        db.session.commit()
        flash("Profil modifié avec succès ✅")
        return redirect(url_for('main.profile'))

    # Remplir les champs
    if request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.age.data = current_user.age
        form.gender.data = current_user.gender
        form.email.data = current_user.email
        form.pseudo.data = current_user.pseudo

    return render_template('update_profile.html', form=form)



@main.route('/confirm_update/<token>')
@login_required
def confirm_update_email(token):
    email = confirm_token(token)
    if not email:
        flash('Lien de confirmation invalide ou expiré.')
        return redirect(url_for('main.profile'))

    update_data = session.get('update_data')
    if not update_data:
        flash('Aucune modification à valider.')
        return redirect(url_for('main.profile'))

    # Mise à jour des informations
    current_user.firstname = update_data['firstname']
    current_user.lastname = update_data['lastname']
    current_user.age = update_data['age']
    current_user.gender = update_data['gender']
    current_user.email = update_data['email']
    current_user.pseudo = update_data['pseudo']

    db.session.commit()
    session.pop('update_data', None)

    flash('Votre profil a été mis à jour et votre email confirmé ✅')
    return redirect(url_for('main.profile'))


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

