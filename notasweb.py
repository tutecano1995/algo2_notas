#!/usr/bin/python
# -*- coding: utf8 -*-

import notas
import web
from web import form

PADRON = "padron"
URL_QUERY = '/consultar'

urls = (
	'/', 'index',
	URL_QUERY, 'query',
)

render = web.template.render('templates/', base='layout', globals={
	'title': "Notas de Algoritmos I",
	'url_query': URL_QUERY,
})

query_form = form.Form(
	form.Textbox(PADRON, 
        	form.notnull,
	        form.regexp('\d+', 'Debe ser un número'),
		description=u"Padrón"
	),
)

class index:
	def GET(self):
		return render.index(query_form())

class query:
	def GET(self):
		f = query_form()
		if not f.validates():
			return render.index(f)
		try:
			return render.result(notas.notas(f[PADRON].value))
		except IndexError, e:
			return render.error(e.message)

if __name__ == "__main__":
	web.application(urls, globals()).run()

