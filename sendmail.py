#!/usr/bin/python
# -*- encoding: utf-8 -*-

import smtplib
import os
from email.mime.text import MIMEText

# para configurar desde afuera
account = os.environ['NOTAS_ACCOUNT']
password = os.environ['NOTAS_PASSWORD']

template = u"""
Este es el link para consultar tus notas:
%s

Nota: El enlace generado es único para tu padrón. No lo compartas con nadie (a menos
que quieras que otros puedan ver tus notas).

-- 
Recibiste este mensaje porque te inscribiste en el sistema de consulta de
notas de Algoritmos I. Si no es así, te pedimos disculpas y por favor ingora este mail.
"""

SendmailException = smtplib.SMTPException

def sendmail(fromname, toaddr, key):
	msg = MIMEText(template % key, _charset="utf-8")
	msg["Subject"] = u'Enlace para consultar las notas'
	msg["From"] = u'%s <%s>' % (fromname, account)
	msg["To"] = toaddr

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login(account, password)
	server.sendmail(account, toaddr, msg.as_string())
	server.close()

