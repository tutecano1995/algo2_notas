# -*- coding: utf-8 -*-

"""Módulo para autenticación con OAuth2."""

import os
import sys

import google.oauth2.service_account
import google.auth.transport.requests

service_account_json = os.environ["NOTAS_SERVICE_ACCOUNT_JSON"]

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/gmail.send"]

_creds = google.oauth2.service_account.Credentials.from_service_account_file(service_account_json, scopes=SCOPES)

def get_credenciales():
    """Devuelve nuestro objeto OAuth2Credentials, actualizado.

    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    if not _creds.valid:
        print("Refrescando token de acceso...", file=sys.stderr)
        _creds.refresh(google.auth.transport.requests.Request())

    return _creds
