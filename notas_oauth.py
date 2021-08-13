# -*- coding: utf-8 -*-

"""Módulo para autenticación con OAuth2."""

import sys

import google.oauth2.service_account
import google.auth.transport.requests

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

_creds = google.oauth2.service_account.Credentials.from_service_account_file("./service_account.json", scopes=SCOPES)

def get_credenciales():
    """Devuelve nuestro objeto OAuth2Credentials, actualizado.

    Esta función llama a _refresh() si el token expira en menos de 5 minutos.
    """
    if not _creds.valid:
        print("Refrescando token de acceso...", file=sys.stderr)
        _creds.refresh(google.auth.transport.requests.Request())

    return _creds
