from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UpdateProfileForm(FlaskForm):
    firstname = StringField('Prénom', validators=[DataRequired(), Length(max=100)])
    lastname = StringField('Nom', validators=[DataRequired(), Length(max=1000)])
    age = IntegerField('Âge')
    gender = StringField('Genre', validators=[Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    pseudo = StringField('Pseudo', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Modifier mon profil')

# Fichier contenant les formulaires et leurs validations (modification profil, inscription, etc.) pour update_profile dans main.py
