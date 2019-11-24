'''run proporciona una cpacidad de enrutamiento de diferentes
URLs para la comunicacion constante del MVC es el archivo de
inicializacion y el que recibe los datos para enviarlos al(los)
 modelos y que este los envie directamente a la base de datos'''
import os
from flask import Flask, render_template,request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, CSRFError
import config
from forms import formArticulo, formCategoria


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


'''@app.route("/articulos/<int:id>")
def mostrar_ariculo(id):
	return 'Vamos a mostrar el artículo con id:{}'.format(id)'''


@app.route('/categorias', methods=['GET'])
def categorias():
    from models import Categorias
    categorias = Categorias.query.all()
    return render_template("index.html", categorias=categorias)


@app.route('/categorias/new', methods=['GET', 'POST'])
def categorias_new():
    from models import Categorias
    form = formCategoria(request.form)
    if form.validate_on_submit():
        cat = Categorias(nombre=form.nombre.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for("categorias"))
    else:
        return render_template("categorias_new.html", form=form)


@app.route('/categorias/<id>', methods=['GET'])
def categoria():
    from models import Categorias, Articulos
    categoria=Categorias.query.get(id)
    if id == '0':
        articulos =Articulos.query.all()
    else:
        articulos=Articulos.query.filter_by(CategoriaID=id)
    categorias=Categorias.query.all()
    return render_template('categorias.html', articulos=articulos, categoria=categoria, categorias=categorias)


@app.route('/articulos/new', methods=['GET', 'POST'])
def articulos_new():
    from models import Articulos, Categorias
    form = formArticulo()
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        try:
            f = form.photo.data
            nombre_fichero = secure_filename(f.filename)
            f.save(app.root_path + "/static/img/" + nombre_fichero)
        except:
            nombre_fichero = ""
        art = Articulos()
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return render_template("upload.html", form=form)


#TODO: no render 'precio'.


'''@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Hemos accedido con POST'
    else:
        return 'Hemos accedido con GET'''


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
