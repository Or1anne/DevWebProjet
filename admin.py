from flask import *
from flask_login import login_required, current_user
from .models import *
from . import db
from datetime import datetime
from fpdf import FPDF
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
        user.email = request.form['email']
        user.pseudo = request.form['pseudo']
        user.lastname = request.form['lastname']
        user.firstname = request.form['firstname']
        user.level = request.form['level']
        user.age = request.form['age']
        user.gender = request.form['gender']
        user.role = request.form['role']
        user.point = request.form['point']

        image_data = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                image_data = image_file.read()
                user.image = image_data

        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d').date()

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
    requests = Request.query.all()
    return render_template('admin_request.html', requests=requests)

@admin.route('/accept/<int:request_id>', methods=['POST'])
def request_accept(request_id):
    request = Request.query.get(request_id)
    if request.title == "Demande de suppression":
        request.status = "Acceptée"
        object = Object.query.filter_by(nom=request.object_name).first()
        db.session.delete(object)
        db.session.commit()
    elif request.title == "Demande d'inscription":
        #TODO Attribuer un rôle à l'utilisateur
        user_data = session.get('user_data')
        user = User(
            email=user_data['email'],
            firstname=user_data['firstname'],
            lastname=user_data['lastname'],
            password=user_data['password'],
            gender=user_data['gender'],
            age=user_data['age'],
            pseudo=user_data['pseudo'],
            birthdate = datetime.strptime(user_data['birthdate'], '%Y-%m-%d').date()
        )
        request.status = "Acceptée"
        db.session.add(user)
        db.session.commit()
    return redirect(url_for('admin.request_admin_list'))

@admin.route('/refuse/<int:request_id>', methods=['POST'])
def request_refuse(request_id):
    request = Request.query.get(request_id)
    if request.title == "Demande de suppression":
        request.status = "Refusée"
        db.session.commit()
    elif request.title == "Demande d'inscription":
        session.pop('user_data', None)
        request.status = "Refusée"
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

    total_energy = db.session.query(db.func.sum(Object.energy)).filter(Object.status == "ON").scalar() or 0
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

    pdf.set_font('Courier', style="B", size=14)
    pdf.cell(195, 10, txt="Liste des objets connectés par Wifi", ln=True, align='C')
    pdf.cell(50, 10, "Nom de l'objet", 1, 0, align='C')
    pdf.cell(40, 10, "Type d'objet", 1, 0, align='C')
    pdf.cell(40, 10, "Marque", 1, 0, align='C')
    pdf.cell(60, 10, "Référence", 1, 1, align='C')

    pdf.set_font('Courier', size=12)
    for object in objects:
        pdf.cell(50, 10, object.nom, 1, 0, 'C')
        pdf.cell(40, 10, object.type, 1, 0, 'C')
        pdf.cell(40, 10, object.brand, 1, 0, 'C')
        pdf.cell(60, 10, object.reference, 1, 1, 'C')
    pdf.ln(5)
    
    pdf.cell(200, 10, txt=f"Nombre d'objets total enregistrés sur la plateforme : {NBobjects}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'objets activés : {NBActivate} ", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'objets non activés : {NBDesactivate} ", ln=True)
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