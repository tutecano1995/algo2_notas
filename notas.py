#!/usr/bin/python
# -*- coding: utf8 -*-

import gdata.spreadsheet.service
import itertools
import collections

# para configurar desde afuera
account = 'aaa@gmail.com'
password = '12345'
spreadsheet_key = '***'

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

def get_feed():
	gd_client = gdata.spreadsheet.service.SpreadsheetsService()
	gd_client.email = account
	gd_client.password = password
	gd_client.source = u'Notas'
	gd_client.ProgrammaticLogin()

	#worksheets = worksheet_dict(gd_client.GetWorksheetsFeed(spreadsheet_key))
	#worksheet_id = worksheets[u'Notas']
	# The first worksheet is always od6
	worksheet_id = 'od6'

	return gd_client.GetCellsFeed(spreadsheet_key, worksheet_id).entry

def notas(padron):
	cells = get_feed()
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
	print notas('942039')

