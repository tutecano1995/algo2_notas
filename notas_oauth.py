# -*- coding: utf-8 -*-

"""Módulo para autenticación con OAuth2."""

import datetime
import httplib2
import os
import sys

import oauth2client.client

_CLIENT_ID = os.environ["NOTAS_OAUTH_CLIENT"]
_CLIENT_SECRET = os.environ["NOTAS_OAUTH_SECRET"]
_OAUTH_REFRESH = os.environ["NOTAS_REFRESH_TOKEN"]

_creds = oauth2client.client.OAuth2Credentials(
    "", _CLIENT_ID, _CLIENT_SECRET, _OAUTH_REFRESH,
    datetime.datetime(2015, 1, 1),
    "https://accounts.google.com/o/oauth2/token", "notasweb/1.0")


def get_credenciales():
    """Devuelve nuestro objeto OAuth2Credentials, actualizado.

    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    now = datetime.datetime.utcnow()
    valid_until = _creds.token_expiry - datetime.timedelta(minutes=5)

    if valid_until < now:
        print("Generando nuevo token de acceso.", file=sys.stderr)
        _creds.refresh(httplib2.Http())

    return _creds
