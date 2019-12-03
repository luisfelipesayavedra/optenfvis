from flask import session, redirect
from run import app


def login_user(usuario):
    session["id"] = usuario.id
    session["username"] = usuario.username
    session["admin"] = usuario.admin


def logout_user():
    session.pop("id", None)
    session.pop("username", None)
    session.pop("admin", None)

def is_login():
    if "id" in session:
        return True
    else:
        return False


def is_admin():
    if "admin"==True:
        return session.get("admin", True)
    else:
        return session.get("admin", False)

@app.context_processor
def login():
    if "id" in session:
        return {'is_login': True}
    else:
        return {'is_login': False}


@app.context_processor
def admin():
    if "admin" == True:
        return session.get("admin", True)
    else:
        return session.get("admin", False)
