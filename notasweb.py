#!/usr/bin/python
# -*- coding: utf8 -*-

import web
import os
from web import form
from email.utils import parseaddr
import hashlib

import notas
import sendmail

TITLE = os.environ['NOTAS_TITLE']

URL_QUERY = '/consultar'

urls = (
	'/?', 'index',
	URL_QUERY + '/?', 'query',
)

render = web.template.render('templates/', base='layout', globals={'title': TITLE, 'ctx': web.ctx})

padron_validator = form.regexp('\d+', u'Ingresar un padrón válido (solo números)')

def error(msg):
	return render.error(unicode(msg))

def genkey(padron):
	secret = 'Penn Premiere'
	return hashlib.sha1(padron + secret).hexdigest()

def genlink(padron):
	return web.ctx.home + URL_QUERY + '?padron=%s&key=%s' % (padron, genkey(padron))

class index:
	form = form.Form(
		form.Textbox('padron', form.notnull, padron_validator, description=u"Padrón"),
		form.Textbox('email', 
			form.notnull,
			form.Validator(u'Ingresar una dirección de mail válida', lambda e: ('@' in e) and bool(parseaddr(e)[1])),
			description=u"e-mail"
		)
	)

	def GET(self):
		return render.index(index.form())

	def POST(self):
		f = index.form()
		if not f.validates():
			return render.index(f)

		if not notas.verificar(f.d.padron, f.d.email):
			f.note = u'La dirección de e-mail no está asociada a ese padrón.'
			return render.index(f)

		try:
			sendmail.sendmail(TITLE, f.d.email, genlink(f.d.padron))
		except sendmail.SendmailException, e:
			return error(e)

		return render.email_sent(f.d.padron, f.d.email)

class query:
	form = form.Form(
		form.Textbox('padron', form.notnull, padron_validator),
		form.Textbox('key', form.notnull),
		validators = (form.Validator('invalid key', lambda f: f.key == genkey(f.padron)),)
	)

	def GET(self):
		f = query.form()
		if not f.validates():
			return error(u"Mmmm... algo salió mal")
		try:
			return render.result(notas.notas(f.d.padron))
		except IndexError, e:
			return error(e.message)

def notfound():
	return web.notfound(error(u'Ruta inválida: ' + web.ctx.path))

app = web.application(urls, locals())
app.notfound = notfound

if __name__ == "__main__":
	app.run()

