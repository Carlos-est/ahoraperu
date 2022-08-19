from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, StringField, PasswordField
from wtforms.validators import Required, DataRequired, Email, Length
from wtforms.fields.html5 import DateField, TimeField
#from wtforms.validators import DataRequired, Email, Length
#from wtforms.fields import DateField, TimeField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets


# login and registration

class LoginForm(FlaskForm):
    email = StringField('Correo',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    nombres = StringField('Nombres:',
                         id='nombre_create',
                         validators=[DataRequired()])

    apellido_paterno = StringField('Apellido paterno:',
                         id='apellidom_create',
                         validators=[DataRequired()])

    apellido_materno = StringField('Apellido materno:',
                         id='apellidom_create',
                         validators=[DataRequired()])

    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])

    ocupacion = StringField('Ocupación:',
                      id='ocupacion_create',
                      validators=[DataRequired(), Email()])
    asociacion = StringField('Asociación:', 
                            id='asociacion_create',
                            validators=[DataRequired(), Email()]) 
    password1 = PasswordField('Contraseña',
                             id='pwd1_create',
                             validators=[DataRequired()])
    password2 = PasswordField('Repite contraseña',
                             id='pwd2_create',
                             validators=[DataRequired()])

class FormIndicadoresCultivo(FlaskForm):
    fechaCosecha = DateField('Indique la fecha de la última cosecha realizada, para calcular la fecha aproximada en que se dio la floración:', format='%Y-%m-%d', validators=(DataRequired(),))
    fechaFloracion = DateField('Indique la fecha de floración más reciente, para proyectar la semana óptima de cosecha:', format='%Y-%m-%d', validators=(DataRequired(),))
    nroSemanas = h5fields.IntegerField("Número de semanas:", widget=h5widgets.NumberInput(min=1, max=56), validators=(DataRequired(),))
    fechaFinal = DateField('Fecha final del periodo:', format='%Y-%m-%d', validators=(DataRequired(),))
    
class FormBiomasa(FlaskForm):
    fechaFloracion = DateField('Fecha de la floración más reciente:', format='%Y-%m-%d', validators=(DataRequired(),))
    fechaCosecha = DateField('Indique la fecha de la última cosecha realizada, para calcular el peso potencial que debió alcanzar el racimo:', format='%Y-%m-%d', validators=(DataRequired(),))
    rPa = h5fields.IntegerField("Densidad de plantas de banano por hectárea (1500-2800):", widget=h5widgets.NumberInput(min=1500, max=2800), validators=(DataRequired(),))
    Cant_manos = h5fields.IntegerField("Número de manos:", widget=h5widgets.NumberInput(min=5, max=13), validators=(DataRequired(),))
    nro_semanas = h5fields.IntegerField(" Número de semanas desde la floración a la cosecha (8-16):", widget=h5widgets.NumberInput(min=8, max=16), validators=(DataRequired(),))
    

class FormNutrientes(FlaskForm):
    fechaCosecha = DateField('Indique la fecha de la última cosecha realizada:', format='%Y-%m-%d', validators=(DataRequired(),))
    rPa = h5fields.IntegerField("Densidad de plantas de banano por hectárea (1500-2800):", widget=h5widgets.NumberInput(min=1500, max=2800), validators=(DataRequired(),))
    intervalo = h5fields.IntegerField("A las cuantas semanas cosechó el racimo (9,10,11,12 o 13):", widget=h5widgets.NumberInput(min=9, max=13), validators=(DataRequired(),))

class FormRiego(FlaskForm):
    dias = h5fields.IntegerField("Número de días que normalmente pasan entre dos riegos (1-45):", widget=h5widgets.NumberInput(min=1, max=45, step=1), validators=(DataRequired(),))
    fechaFinal = DateField('Fecha final del periodo:', format='%Y-%m-%d', validators=(DataRequired(),))