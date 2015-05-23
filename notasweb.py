#!/usr/bin/env python3

import os
import hashlib

import flask
import flask_wtf

from wtforms import fields
from wtforms import validators
from wtforms.fields import html5

import notas
import sendmail

app = flask.Flask(__name__)
app.secret_key = os.environ["NOTAS_SECRET"]
app.config.title = "Notas de " + os.environ["NOTAS_COURSE_NAME"]

assert app.secret_key


class Formulario(flask_wtf.Form):
    """Pide el padrón y la dirección de correo.
    """
    padron = fields.StringField(
        "Padrón", validators=[
            validators.Regexp(r"\w+", message="Ingresár un padrón válido")])

    email = html5.EmailField(
        "E-mail", validators=[
            validators.Email(message="Ingresar una dirección de mail válida")])

    submit = fields.SubmitField("Obtener enlace")


@app.route("/", methods=('GET', 'POST'))
def index():
    form = Formulario()

    if form.validate_on_submit():
        padron = norm_field(form.padron)
        email = norm_field(form.email)

        if not notas.verificar(padron, email):
            flask.flash(
                "La dirección de mail no está asociada a ese padrón", "danger")
        else:
            try:
                sendmail.sendmail(app.config.title, email, genlink(padron))
            except sendmail.SendmailException as e:
                return flask.render_template("error.html", message=str(e))
            else:
                return flask.render_template("email_sent.html", email=email)

    return flask.render_template("index.html", form=form)


@app.route("/consultar")
def consultar():
    try:
        key = flask.request.args["key"]
        padron = flask.request.args["padron"]
    except KeyError as e:
        return flask.render_template(
            "error.html",
            message="Error: URL de consulta no válida ({})".format(e))

    if key != genkey(padron):
        return flask.render_template(
            "error.html",
            message="Error: parametro ‘padron’ o ‘key’ no válidos")

    try:
        notas_alumno = notas.notas(padron)
    except IndexError as e:
        return flask.render_template("error.html", message=str(e))
    else:
        return flask.render_template("result.html", items=notas_alumno)


def norm_field(f):
    """Devuelve los datos del campo en minúsculas y sin espacio alreadedor.
    """
    return f.data.strip().lower()


def genkey(padron):
    """Devuelve la clave asociada con un padrón.
    """
    secret = (padron + app.secret_key).encode("utf-8")
    return hashlib.sha1(secret).hexdigest()


def genlink(padron):
    """Devuelve la dirección de consulta de un padrón.
    """
    return flask.url_for("consultar", padron=padron, key=genkey(padron),
                         _external=True)


if __name__ == "__main__":
    app.run(debug=True)
