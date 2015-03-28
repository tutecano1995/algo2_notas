#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO: migrar de SpreadsheetsService a SpreadsheetsClient.
import gdata.spreadsheet.service
import itertools
import os

import notas_oauth

# para configurar desde afuera
SPREADSHEET_KEY = os.environ["NOTAS_SPREADSHEET_KEY"]

def worksheet_dict(feed):
	d = {}
	for i, entry in enumerate(feed.entry):
		d[entry.title.text] = entry.id.text.split('/')[-1]
	return d

def get_header(row):
	keys = []
	for i, cell in enumerate(row):
		keys.append(cell.cell.text)
	return keys

def get_row_data(row, keys):
	data = [ (k, '') for k in keys ]
	for cell in row:
		i = int(cell.cell.col) - 1
		data[i] = (keys[i], cell.cell.text)
	return data

def find_cell(data, key):
	for k, v in data:
		if k == key:
			return v
	return None

def connect():
	# En general SpreadsheetsService no es compatible con OAuth 2.0
	# (solamente 1.0), pero si ponemos a mano el header Bearer, funciona:
	# http://stackoverflow.com/a/29157967/848301.
        token = notas_oauth.access_token()
	client = gdata.spreadsheet.service.SpreadsheetsService(
	        additional_headers={'Authorization': 'Bearer %s' % token})

	return client

def worksheet_id(client, worksheet_name):
	worksheets = worksheet_dict(client.GetWorksheetsFeed(SPREADSHEET_KEY))
	return worksheets[worksheet_name]

def GetListFeed(worksheet_name):
	client = connect()
	return client.GetListFeed(SPREADSHEET_KEY, worksheet_id(client, worksheet_name)).entry

def GetCellsFeed(worksheet_name):
	client = connect()
	return client.GetCellsFeed(SPREADSHEET_KEY, worksheet_id(client, worksheet_name)).entry

def verificar(padron, email):
	rows = GetListFeed(u'DatosAlumnos')
	for row in rows:
		if row.custom[u'padrón'].text == padron and row.custom[u'email'].text.lower() == email.lower():
			return True
	return False

def notas(padron):
	cells = GetCellsFeed(u'Notas')
	keys = None
	PADRON = 'Padrón'
	for _, row in itertools.groupby(cells, lambda cell: cell.cell.row):
		if keys is None:
			keys = get_header(row)
			continue
		data = get_row_data(row, keys)
		p = find_cell(data, PADRON)
		if not p:
			break
		if p == padron:
			return data
	raise IndexError(u'Padrón %s no encontrado' % padron)

if __name__ == '__main__':
	print verificar('942039', 'aaa')

