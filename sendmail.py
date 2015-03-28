#!/usr/bin/python
# -*- coding: utf-8 -*-

import base64
import smtplib
import os
from email.mime.text import MIMEText

import notas_oauth

# para configurar desde afuera
COURSE = os.environ['NOTAS_COURSE_NAME']
ACCOUNT = os.environ['NOTAS_ACCOUNT']

template = u"""
Este es el link para consultar tus notas:
%s

Nota: El enlace generado es único para tu padrón. No lo compartas con nadie (a menos
que quieras que otros puedan ver tus notas).

-- 
Recibiste este mensaje porque te inscribiste en el sistema de consulta de
notas de %s. Si no es así, te pedimos disculpas y por favor ingora este mail.
"""

SendmailException = smtplib.SMTPException

def sendmail(fromname, toaddr, key):
	msg = MIMEText(template % (key, COURSE), _charset="utf-8")
	msg["Subject"] = u'Enlace para consultar las notas'
	msg["From"] = u'%s <%s>' % (fromname, ACCOUNT)
	msg["To"] = toaddr

	xoauth2_tok = "user=%s\1" "auth=Bearer %s\1\1" % (
	        ACCOUNT, notas_oauth.access_token())
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(xoauth2_tok))
	server.sendmail(ACCOUNT, toaddr, msg.as_string())
	server.close()

