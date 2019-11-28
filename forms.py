from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField,TextAreaField, SelectField, PasswordField, HiddenField
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