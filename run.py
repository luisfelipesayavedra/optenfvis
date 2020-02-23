import os
from flask import Flask, render_template,request, redirect,url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect, CSRFError
import config
from forms import formArticulo, formCategoria, formBnB, formLogin, formRegistro
import pyrebase


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'ZgI3| Krz=9: 8RbP |6c|;'
PWD = os.path.abspath(os.curdir)
csrf = CSRFProtect(app)

firebaseConfig = {
    "apiKey": "AIzaSyCSA4YAGmrAZo8jU4HFGI1UgEmLOZbR2v4",
    "authDomain": "enfovisual-efe58.firebaseapp.com",
    "databaseURL": "https://enfovisual-efe58.firebaseio.com",
    "projectId": "enfovisual-efe58",
    "storageBucket": "enfovisual-efe58.appspot.com",
    "messagingSenderId": "59273870243",
    "appId": "1:59273870243:web:9b400bd65f7e23e850b816"
  }

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


@app.route('/') #URL principal de la aplicacion que indexa al archivo raiz
def home():
    from models import Articulos, Categorias
    articulos = Articulos.query.all()
    categorias = Categorias.query.all()
    return render_template('index.html', articulos=articulos, categorias=categorias)


@app.route('/sitemap.xml')
def sitemap():
    return render_template('sitemap.xml')


@app.route('/robots.txt')
def robots():
    return render_template('robots.txt')


@app.route('/op_img')
def op_img():
    if request.args.get('type') == '1':
       filename = 'static/inimg/op-img.jpg'
    else:
       filename = 'static/inimg/op-img.jpg'
    return send_file(filename, mimetype='image/jpg')


@app.route('/admintab')
def admintab():
    from models import Articulos, Categorias
    categorias = Categorias.query.all()
    articulos = Articulos.query.all()
    return render_template('articulos_admin.html', categorias=categorias, articulos=articulos)


@app.route('/articulos/new', methods=['GET', 'POST'])
def articulos_new():
    global nombre_fichero
    from models import Articulos, Categorias
    from login import is_admin

    if not is_admin():
        abort(404)
        return render_template('404.html')

    form = formArticulo()
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias

    if form.validate_on_submit():
        try:
            f = form.photo.data
            nombre_fichero = secure_filename(f.filename)

            upload = request.files["photo"]
            storage.child('images/' + nombre_fichero).put(upload)
        except:
            nombre_fichero = ""

        imglink = storage.child('images/' + nombre_fichero).get_url(None)
        art = Articulos()
        form.populate_obj(art)
        art.image = imglink
        current_db_session = db.session.object_session(art)
        db.session.add(art)
        db.session.commit()
        return redirect(url_for("admintab"))

    else:
        return render_template("upload.html", form=form)


@app.route('/articulos/<id>/edit', methods=['GET', 'POST'])
def articulos_edit(id):
    from models import Articulos, Categorias
    from login import is_admin
    art = Articulos.query.get(id)
    if art is None and not is_admin:
        abort(404)
        return render_template('404.html')
    form = formArticulo(obj=art)
    categorias = [(c.id, c.nombre) for c in Categorias.query.all()[1:]]
    form.CategoriaId.choices = categorias
    if form.validate_on_submit():
        try:
            f = form.photo.data
            nombre_fichero = secure_filename(f.filename)

            upload = request.files["photo"]
            storage.child('images/' + nombre_fichero).put(upload)
        except:
            nombre_fichero = ""
        else:
            nombre_fichero = storage.child('images/' + nombre_fichero).get_url(None)
        form.populate_obj(art)
        art.image = nombre_fichero
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('upload.html', form=form)


@app.route('/ariticulos/<id>/delete', methods=['GET', 'POST'])
def articulos_delete(id):
    from models import Articulos
    from login import is_admin

    art = Articulos.query.get(id)

    if art is None:
        return "<h1>No existe el archivo</h2>"

    if not is_admin():
        return render_template('404.html')

    form = formBnB()

    if form.validate_on_submit():
        if form.borrar.data:
            if art.image != "":
                os.remove(app.root_path+"/static/img/"+art.image)
            else:
                form.borrar.data(art)
    current_db_session = db.session.merge(art)
    db.session.delete(current_db_session)
    db.session.commit()
    return redirect(url_for("admintab"))
    return render_template("articulos_delete.html", form=form, art=art)


@app.route('/categorias/new', methods=['GET', 'POST'])
def categorias_new():
    from models import Categorias
    form = formCategoria(request.form)
    if form.validate_on_submit():
        cat = Categorias(nombre=form.nombre.data)
        db.session.add(cat)
        db.session.commit()
        return redirect(url_for("admintab"))
    else:
        return render_template("categorias_new.html", form=form)


@app.route('/categorias/<id>/edit', methods=['POST', 'GET'])
def categorias_edit(id):
    from models import Categorias
    cat=Categorias.query.get(id)
    if cat is None:
        Abort(404)
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
        return "<h1>No existe la categoria</h2>"

    form = formBnB()

    if form.validate_on_submit():
        if form.borrar.data:
            current_db_session = db.session.merge(cat)
            db.session.delete(current_db_session)
            db.session.commit()
        return redirect(url_for('admintab'))
    return render_template('categorias_delete.html', form=form, cat=cat)


@app.route('/login', methods=['GET', 'POST'])
def login():
    from models import Usuarios
    from login import login_user, is_login
    if is_login():
        return redirect(url_for("home"))
    form = formLogin()
    if form.validate_on_submit():
        user=Usuarios.query.filter_by(username=form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        form.username.errors.append("usuario o contraseña incorrecta")
    return render_template('login.html', form=form)


@app.route("/logout", methods=['get'])
def logout():
    from login import logout_user
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    from models import Usuarios
    form = formRegistro()
    if form.validate_on_submit():
        user_exist = Usuarios.query.\
            filter_by(username=form.username.data).first()
        if user_exist is None and form.password_c is form.password:
            user=Usuarios()
            form.populate_obj(user)
            user.admin = False
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
        elif form.password_c is not form.password:
                form.password.errors.append("la contraseña no coincide")
        else:
            form.username.errors.append("Nombre de Usuario en uso")
    return render_template('signup_form.html', form=form)


@app.route('/perfil/<username>', methods=["get", "post"])
def perfil(username):
    from models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = formRegistro(request.form, obj=user)
    del form.password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("signup_form.html", form=form, perfil=True)


'''@app.route('/changepassword/<username>', methods=["get", "post"])
def changepassword(username):
    from aplicacion.models import Usuarios
    user = Usuarios.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    form = FormChangePassword()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("changepassword.html", form=form)'''
#TODO:crear la pagina para cambiar la contraseña y que inicie sesion cuando se registre


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")

@app.route('/politicasdeprivacidad/')
def politicasdeprivacidad():
    return render_template('politicas_de_privacidad.html')


if __name__ == '__main__':
    app.run()