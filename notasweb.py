#!/usr/bin/env python3

import os
import hashlib

import flask
import flask_wtf

from webargs import Arg, ValidationError
from webargs.flaskparser import FlaskParser

from wtforms import fields
from wtforms import validators
from wtforms.fields import html5

import notas
import sendmail

app = flask.Flask(__name__)
app.secret_key = os.environ["NOTAS_SECRET"]
app.config.title = "Notas de " + os.environ["NOTAS_COURSE_NAME"]

assert app.secret_key


@app.errorhandler(400)
def bad_request(err):
    return flask.render_template(
        "error.html", message=str(err.data["message"])), 400


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
    args = {
        "key": Arg(str, required=True),
        "padron": Arg(str, required=True),
    }
    def validar(args):
        if args["key"] == genkey(args["padron"]):
            return True
        else:
            raise ValidationError("Parámetro ‘padron’ o ‘key’ no válido")

    result = FlaskParser().parse(args, validate=validar)

    try:
        notas_alumno = notas.notas(result["padron"])
    except (IndexError, KeyError) as e:
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
