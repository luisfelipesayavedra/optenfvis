from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField, \
    TextAreaField, SelectField, PasswordField, HiddenField
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Required, NumberRange


class UploadForm(FlaskForm):
    photo = FileField('selecciona imagen:', validators=[FileRequired()])
    submit = SubmitField('Submit')
