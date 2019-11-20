#run proporciona una cpacidad de enrutamiento de diferentes URLs para la comunicacion constante del MVC es el archivo de inicializacion y el que recibe los datos para enviarlos al(los) modelos y que este los envie directamente a la base de datos
import os
from flask import Flask, render_template,request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, CSRFError
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'ZgI3| Krz=9: 8RbP |6c|;'
PWD = os.path.abspath(os.curdir)
csrf = CSRFProtect(app)


@app.route('/') #URL principal de la aplicacion que indexa al archivo raiz
def home():
    from models import Articulos
    articulos=Articulos.query.all()
    return render_template('index.html', articulos=articulos)


@app.route('/articulos/')
def articulos():
    return 'lista de articulos'


@app.route('/articulos/new', methods=["POST"])
def articulos_new():
    return 'Está URL recibe información de un formulario con el método POST'


'''@app.route("/articulos/<int:id>")
def mostrar_ariculo(id):
	return 'Vamos a mostrar el artículo con id:{}'.format(id)'''


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    from forms import UploadForm
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(app.root_path + "/static/img/" + filename)
        return 'saved' #redirect(url_for('home'))
    return render_template('send_img.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Hemos accedido con POST'
    else:
        return 'Hemos accedido con GET'


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
