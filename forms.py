from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField,TextAreaField, SelectField, PasswordField, HiddenField, BooleanField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, NumberRange


class formCategoria(FlaskForm):
   nombre = StringField("Nombre:",
                        validators=[Required("Tienes que introducir el dato")]
                        )
   submit = SubmitField('Enviar')


class formArticulo(FlaskForm):
   nombre=StringField("Nombre:", validators=[Required("Tienes que introducir el dato")])
   precio=IntegerField("Precio:", default=0, validators=[Required("Tienes que introducir el dato")])
   descripcion= TextAreaField("Descripción:")
   photo = FileField('Selecciona imagen:', validators=[Required("tienes que enviar las imagenes")])
   wppurl =StringField("enlace de whatsapp")
   CategoriaId=SelectField("Categoría:", coerce=int)
   submit = SubmitField('Enviar')


class formBnB(FlaskForm):
    borrar = SubmitField('borrar')
    noborrar = SubmitField('no borrar')


class formLogin(FlaskForm):
      username = StringField('Login', validators=[Required()])
      password = PasswordField('Password', validators=[Required()])
      submit = SubmitField('Entrar')


class formRegistro(FlaskForm):
    username = StringField('username', validators=[Required()])
    password = PasswordField('contraseña', validators=[Required()])
    password_c = PasswordField('confirmar contraseña', validators=[Required()])
    nombre = StringField('nombre', validators=[Required()])
    email = StringField('email', validators=[Required()])
    checkbox = BooleanField(' ', validators=[Required()])
    submit = SubmitField('Registrarse')
