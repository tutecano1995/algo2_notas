#!/usr/bin/python
# -*- coding: utf8 -*-

import notas
import web
from web import form
from email.utils import parseaddr
import smtplib
import hashlib

URL_QUERY = '/consultar'

urls = (
	'/', 'index',
	URL_QUERY, 'query',
)

render = web.template.render('templates/', base='layout', globals={
	'title': "Notas de Algoritmos I",
})

padron_validator = form.regexp('\d+', u'Ingresar un padrón válido (solo números)')

def genkey(padron):
	secret = 'Penn Premiere'
	return hashlib.sha1(padron + secret).hexdigest()

def genlink(padron):
	return web.ctx.homedomain + URL_QUERY + '?padron=%s&key=%s' % (padron, genkey(padron))

class index:
	form = form.Form(
		form.Textbox('padron', form.notnull, padron_validator, description=u"Padrón"),
		form.Textbox('email', 
			form.notnull,
			form.Validator(u'Ingresar una dirección de mail válida', lambda e: ('@' in e) and bool(parseaddr(e)[1])),
			description=u"e-mail"
		),
	)

	def GET(self):
		return render.index(index.form())

	def POST(self):
		f = index.form()
		if not f.validates():
			return render.index(f)

		try:
			self.enviar_mail(f.d.padron, f.d.email)
		except smtplib.SMTPException, e:
			return render.error(e.message)

		return render.email_sent(f.d.padron, f.d.email, genlink(f.d.padron))

	def enviar_mail(self, padron, email):
		pass

class query:
	form = form.Form(
		form.Textbox('padron', form.notnull, padron_validator),
		form.Textbox('key', form.notnull),
		validators = (form.Validator('invalid key', lambda f: f.key == genkey(f.padron)),)
	)

	def GET(self):
		f = query.form()
		if not f.validates():
			return render.error(u"Mmmm... algo salió mal")
		try:
			return render.result(notas.notas(f.d.padron))
		except IndexError, e:
			return render.error(e.message)

if __name__ == "__main__":
	web.application(urls, globals()).run()

