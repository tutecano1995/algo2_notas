#!/usr/bin/python
# -*- coding: utf8 -*-

import gdata.spreadsheet.service
import itertools
import collections
import os

# para configurar desde afuera
account = os.environ['NOTAS_ACCOUNT']
password = os.environ['NOTAS_PASSWORD']
spreadsheet_key = os.environ['NOTAS_SPREADSHEET_KEY']

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
	data = collections.OrderedDict()
	for k in keys:
		data[k] = ''
	for cell in row:
		i = int(cell.cell.col) - 1
		data[keys[i]] = cell.cell.text
	return data

def connect():
	client = gdata.spreadsheet.service.SpreadsheetsService()
	client.email = account
	client.password = password
	client.source = u'Notas'
	client.ProgrammaticLogin()
	return client

def worksheet_id(client, worksheet_name):
	worksheets = worksheet_dict(client.GetWorksheetsFeed(spreadsheet_key))
	return worksheets[worksheet_name]

def GetListFeed(worksheet_name):
	client = connect()
	return client.GetListFeed(spreadsheet_key, worksheet_id(client, worksheet_name)).entry

def GetCellsFeed(worksheet_name):
	client = connect()
	return client.GetCellsFeed(spreadsheet_key, worksheet_id(client, worksheet_name)).entry

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
		if PADRON not in data:
			break
		if data[PADRON] == padron:
			return data
	raise IndexError(u'Padrón %s no encontrado' % padron)

if __name__ == '__main__':
	print verificar('942039', 'aaa')

