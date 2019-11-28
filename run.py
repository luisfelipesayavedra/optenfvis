import os
from flask import Flask, render_template,request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, CSRFError
import config
from forms import formArticulo, formCategoria, formBnB


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


@app.route('/articulos/<id>/edit', methods=['GET', 'POST'])
def articulos_edit(id):
    from models import Articulos, Categorias
    art = Articulos.query.get(id)
    if art is None:
        abort(404)
    form = formArticulo(obj=art)
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        if form.photo.data:
            os.remove(app.root_path+"static/img"+art.image)
            try:
                f = form.photo.data
                nombre_fichero = secure_filename(f.filename)
                f.save(app.root_path+"/static/img"+nombre_fichero)
            except:
                nombre_fichero=""
        else:
            nombre_fichero = art.image
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('upload.html', form=form)


@app.route('/ariticulos/<id>/delete', methods=['GET', 'POST'])
def articulos_delete(id):
    from models import Articulos
    art=Articulos.query.get(id)
    if art is None:
        abort(404)
    form = formBnB()
    if form.validate_on_submit():
        if form.borrar.data:
            if art.image != "":
                os.remove(app.root_path+"/static/img/"+art.image)
            current_db_session = db.session.object_session(art)
            current_db_session.delete(art)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("articulos_delete.html", form=form, art=art)

@app.route('/categorias/', methods=['GET'])
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


@app.route('/categorias/<id>/edit', methods=['POST', 'GET'])
def categorias_edit(id):
    from models import Categorias
    cat=Categorias.query.get(id)
    if cat is None:
        abort(404)
    form = formCategoria(request.form, obj=cat)
    if form.validate_on_submit():
        form.populate_obj(cat)
        db.session.commit()
        return render_template('categorias.html',)
    return render_template('categorias_new.html', form=form)


@app.route('/categorias/<id>/delete', methods=['POST', 'GET'])
def categorias_delete(id):
    from models import Categorias
    cat = Categorias.query.get(id)
    if cat is None:
        abort(404)
    form = formBnB()
    if form.validate_on_submit():
        if form.borrar.data:
            current_db_session = db.session.object_session(cat)
            current_db_session.delete(cat)
            db.session.commit()
        return redirect(url_for('categorias'))
    return render_template('categorias_delete.html', form=form, cat=cat)


'''def login():
    if request.method == 'POST':
        return 'Hemos accedido con POST'
    else:
        return 'Hemos accedido con GET'''


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)