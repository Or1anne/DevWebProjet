from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db
from datetime import datetime
from sqlalchemy import *
from fpdf import FPDF
from werkzeug.security import generate_password_hash, check_password_hash
from tempfile import NamedTemporaryFile

admin = Blueprint('admin', __name__)

#Gestion des utilisateurs
@admin.route('/gestion')
def gestion_utilisateur():
    users = User.query.all()
    return render_template('admin_gestion_utilisateur.html', users=users)

@admin.route('/userProfile/<int:user_id>')
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('admin_user_profile.html', user=user)

@admin.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    
    user = User.query.get(user_id)

    if request.method == 'POST':

        pseudo = request.form['pseudo']
        existing_pseudo = User.query.filter(User.pseudo == pseudo, User.id != user.id ).first()
        if existing_pseudo:
            flash("Ce pseudo est déjà utilisé, veuillez en choisir un autre.")
            return redirect(url_for('admin.edit_user', user_id=user.id))
        else :
            user.pseudo = pseudo

        email = request.form['email']
        existing_email = User.query.filter(User.email == email, User.id != user.id).first()
        if existing_email:
            flash("Cette adresse email est déjà utilisée, veuillez en choisir une autre.")
            return redirect(url_for('admin.edit_user', user_id=user.id))
        else :
            user.email = email
        
        user.lastname = request.form['lastname']
        user.firstname = request.form['firstname']
        user.level = request.form['level']
        user.gender = request.form['gender']
        user.role = request.form['role']
        user.point = request.form['point']
        if current_user.password != request.form['password']:
            current_user.password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                user.image = image_data

        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()
        user.birthdate = birthdate

        today = datetime.today()
        user.age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        db.session.commit()
        return redirect(url_for('admin.gestion_utilisateur'))

    return render_template('admin_edit_user.html', user=user)

@admin.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('admin.gestion_utilisateur'))

#Requêtes d'admin
@admin.route('/request_admin')
def request_admin_list():
    q = request.args.get('q', '')
    requests = Request.query.filter(
        or_(
            Request.title.ilike(f'%{q}%'),
            Request.object_name.ilike(f'%{q}%'),
            Request.description.ilike(f'%{q}%'),
            cast(Request.date, String).ilike(f'%{q}%')
        )
    ).order_by(desc(Request.date)).all()
    return render_template('admin_request.html', requests=requests)

@admin.route('/accept/<int:request_id>', methods=['POST'])
def request_accept(request_id):
    rqs = Request.query.get(request_id)
    if rqs.title == "Demande de suppression d'objet":
        rqs.status = "Acceptée"
        object = Object.query.filter_by(nom=rqs.object_name).first()
        db.session.delete(object)
        db.session.commit()
    elif rqs.title == "Demande de suppression de pièce":
        rqs.status = "Acceptée"
        room = Room.query.filter_by(nom=rqs.object_name).first()
        db.session.delete(room)
        db.session.commit()
    elif rqs.title == "Demande de passage à niveau":
        rqs.status = "Acceptée"
        user = User.query.get(rqs.object_type)

        if user.level == "Debutant" and user.point >= 100:
            user.level = "Intermediaire"
            user.point -= 100
        elif user.level == "Intermediaire" and user.point >= 500:
            user.level = "Avance"
            user.point -= 500
        elif user.level == "Avance" and user.point >= 1000:
            user.level = "Expert"
            user.point -= 1000
        else : 
            flash(user.pseudo + " n'a pas assez de points pour passer au niveau supérieur.")
            return redirect(url_for('admin.request_admin_list'))
        db.session.commit()
    elif rqs.title == "Demande d'inscription":
        user_data = session.get('user_data')
        user = User(
            email=user_data['email'],
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            password=user_data['password'],
            gender=user_data['gender'],
            age=user_data['age'],
            pseudo=user_data['pseudo'],
            birthdate = user_data['birthdate'],
            role = request.form.get('role'),
            confirmed=True
        )
        rqs.status = "Acceptée"
        db.session.add(user)
        db.session.commit()
        session.pop('user_data', None)
    return redirect(url_for('admin.request_admin_list'))

@admin.route('/refuse/<int:request_id>', methods=['POST'])
def request_refuse(request_id):
    request = Request.query.get(request_id)
    if request.title == "Demande de suppression d'objet" or request.title == "Demande de suppression de pièce" or request.title == "Demande de passage à niveau":
        request.status = "Refusée"
        db.session.commit()
    elif request.title == "Demande d'inscription":
        session.pop('user_data', None)
        request.status = "Refusée"
        db.session.commit()
    return redirect(url_for('admin.request_admin_list'))

@admin.route('/delete_request/<int:request_id>', methods=['POST'])
def delete_request(request_id):
    request = Request.query.get(request_id)
    if request:
        db.session.delete(request)
        db.session.commit()
    return redirect(url_for('admin.request_admin_list'))

#Rapport statistique
@admin.route('/rapport')
def rapport():
    users = User.query.all()
    objects = Object.query.all()
    rooms = Room.query.all()

    NBusers = User.query.count()
    NBobjects = Object.query.count()
    NBrooms = Room.query.count()

    NBActivate = Object.query.filter_by(status="ON").count()
    NBDesactivate = Object.query.filter_by(status="OFF").count()
    NBError = Object.query.filter_by(battery=0).count()

    total_energy = db.session.query(db.func.sum(Object.energy)).filter(Object.status == "ON", Object.battery != 0).scalar() or 0
    total_luminosity = db.session.query(db.func.sum(Object.luminosity)).filter(Object.status == "ON").scalar() or 0

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Courier', style="B", size=24)

    pdf.cell(200, 10, 'Rapport Statistique', ln=True, align='C')
    pdf.ln(5)

    pdf.set_font('Courier', size=12)
    pdf.cell(200, 10, txt=f"Date de création du rapport : {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Nombre de pièces dans la maison : {NBrooms}", ln=True)
    pdf.ln(5)

    pdf.set_font('Courier', style="B", size=14)
    pdf.cell(195, 10, txt="Liste des utilisateurs", ln=True, align='C')
    pdf.cell(40, 10, "Pseudo", 1, 0, align='C')
    pdf.cell(40, 10, "Nom", 1, 0, align='C')
    pdf.cell(40, 10, "Prénom", 1, 0, align='C')
    pdf.cell(30, 10, "Âge", 1, 0, align='C')
    pdf.cell(40, 10, "Rôle", 1, 1, align='C')

    pdf.set_font('Courier', size=12)
    for user in users:
        pdf.cell(40, 10, user.pseudo, 1, 0, 'C')
        pdf.cell(40, 10, user.lastname, 1, 0, 'C')
        pdf.cell(40, 10, user.firstname, 1, 0, 'C')
        pdf.cell(30, 10, str(user.age), 1, 0, 'C')
        pdf.cell(40, 10, user.role if user.role else "Non attribué", 1, 1, 'C')
    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Nombre d'utilisateurs incrits sur la plateforme : {NBusers}", ln=True)
    pdf.ln(5)

    pdf.set_font('Courier', style="B", size=10)
    pdf.cell(195, 10, txt="Liste des objets dans la maison", ln=True, align='C')
    pdf.cell(40, 10, "Nom de l'objet", 1, 0, align='C')
    pdf.cell(40, 10, "Type d'objet", 1, 0, align='C')
    pdf.cell(30, 10, "Marque", 1, 0, align='C')
    pdf.cell(40, 10, "Référence", 1, 0, align='C')
    pdf.cell(40, 10, "Pièce assignée", 1, 1, align='C')

    pdf.set_font('Courier', size=8)
    for object in objects:
        pdf.cell(40, 10, object.nom, 1, 0, 'C')
        pdf.cell(40, 10, object.type, 1, 0, 'C')
        pdf.cell(30, 10, object.brand, 1, 0, 'C')
        pdf.cell(40, 10, object.reference, 1, 0, 'C')
        pdf.cell(40, 10, object.room.nom if object.room else "Non assignée", 1, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font('Courier', size=12)
    pdf.cell(200, 10, txt=f"Nombre d'objets total enregistrés sur la plateforme : {NBobjects}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'objets activés : {NBActivate} ", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'objets non activés : {NBDesactivate} ", ln=True)
    pdf.ln(1)

    pdf.cell(200, 10, txt=f"Nombre d'objets dysfonctionnels (Plus de batterie) : {NBError} ", ln=True)

    pdf.ln(5)

    pdf.set_font('Courier',style="BU", size=14)
    pdf.cell(200, 10, txt="Consommation énergétique totale", ln=True)
    pdf.ln(5)

    pdf.set_font('Courier', size=12)
    pdf.cell(200, 10, txt=f"Consommation électrique : {total_energy} Wh", ln=True)
    pdf.cell(200, 10, txt=f"Consommation lumineuse : {total_luminosity} Lm", ln=True)

    with NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        pdf.output(temp_file.name)
        temp_file.close()  # Fermer le fichier temporaire pour éviter les erreurs

        # Utiliser send_file pour envoyer le fichier au client
        return send_file(temp_file.name, as_attachment=True, download_name="Rapport_Statistique.pdf", mimetype="application/pdf")