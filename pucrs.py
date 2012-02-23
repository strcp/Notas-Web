#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of Notas-Web. Notas-Web is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY. See the GNU General Public License for more details

import urllib
import urllib2
import getopt
import sys
import simplejson
import json
import string
import unicodedata as ud
from BeautifulSoup import BeautifulSoup
from django.http import HttpResponse

def RepresentsFloat(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

class Aluno:
	def __init__(self):
		self.info = {}

	def breakdown(self, string):
		romans = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]

		if string is None:
			return ""

		n = string.split()
		p = ""
		for i in n:
			if i in romans:
				i = i.upper()
			p = p + " " + i
		p = p.lstrip()
		return p

	def parseGrausData(self, soup):
		cursos = []

		if soup is None:
			return self.info

		tmp = soup.find(text = "Nome do Aluno:")
		if tmp is not None:
			self.info['nome'] = tmp.next.string.strip().title()

		tmp = soup.find(text = u'Matrícula:')
		if tmp is not None:
			self.info['matricula'] = tmp.next.string.strip().replace('-', '')

		curso = self.createCurso(soup)
		cursos.append(curso)

		#self._data['self.info'] = self.info
		self.info['cursos'] = cursos

		return self.info

	def createNota(self, tipo = None, valor = None, data = None):
		if ((valor is None) or (valor == "")):
			return None;

		nota = {}
		nota['tipo'] = tipo

		if (data is not None) and len(data) > 0:
			nota['data'] = data
		else:
			nota['data'] = None

		if valor == ud.normalize('NFC', u"N\u00e3o publicado"):
			nota['valor'] = "-"
		else:
			nota['valor'] = valor

		return nota

	def createDisciplina(self, discdata):
		disc = {}
		disc['nome'] = None
		disc['notas'] = None
		notas = []

		if len(discdata) < 1:
			return disc

		tmp_nome = discdata[0]('td', {'rowspan':'3', 'align':'left', 'valign':'center'})[0].b.text.capitalize()
		disc['nome'] = self.breakdown(tmp_nome)

		tmp = discdata[0].table

		# Notas
		x = 0
		for tipos in tmp.contents[0]('th'):
			tipo = tipos.text
			if (len(tmp) > 1):
				valores = tmp.contents[1].findAll('td')

				if RepresentsFloat(valores[x].text):
					valor = valores[x].text
				else:
					valor = None

			if (len(tmp) > 2):
				datas = tmp.contents[2].findAll('td')
				data = datas[x].text
			x += 1
			nota = self.createNota(tipo, valor, data)
			if nota is not None:
				notas.append(nota)

		tmp1 = discdata[0].next
		if (len(discdata) > 1):
			tmp2 = discdata[1]
		else:
			tmp2 = None

		# G1 e G2
		i = 0
		while (tmp1 is not None):
			if i == 11:
				if RepresentsFloat(tmp1.text) or tmp1.text == "NC":
					valor = tmp1.text
				else:
					valor = None

				if ((tmp2 is not None) and (len(tmp2.contents) > 3)):
					data = tmp2.contents[1].text

				nota = self.createNota("G1", valor, data)
				if nota is not None:
					notas.append(nota)
			elif i == 13:

				if RepresentsFloat(tmp1.text) or tmp1.text == "NC":
					valor = tmp1.text
				else:
					valor = None

				if ((tmp2 is not None) and (len(tmp2.contents) > 3)):
					data = tmp2.contents[3].text

				nota = self.createNota("G2", valor, data)
				if nota is not None:
					notas.append(nota)

			tmp1 = tmp1.nextSibling
			i += 1

		# Final

		valor = discdata[0]('td', {'rowspan':'2', 'align':'center', 'valign':'center'})[2].text

		if RepresentsFloat(valor) or valor == "REP":
			nota = self.createNota("Final", valor)
			if nota is not None:
				notas.append(nota)

		disc['notas'] = notas

		return disc

	def createCurso(self, soup):
		disciplinas = []
		curso = {}

		if soup is None:
			return curso

		curso['disciplinas'] = disciplinas

		tmp = soup.find(text = "Curso:")
		cursop = tmp.next.string.split('-', 2)

		curso['cod'] = cursop[0].strip()
		curso['nome'] = cursop[1].strip()

		tmp = None
		tmp = soup.html.body.table

		if tmp is None:
			return curso

		while ('\n' in tmp):
			tmp.contents.remove('\n')

		tmp.contents.remove(tmp.contents[0])
		tmp.contents.remove(tmp.contents[len(tmp) - 1])
		ndisc = (len(tmp) / 3)

		if ndisc == 0:
			return curso

		y = 0
		for t in range(ndisc):
			disciplina = self.createDisciplina(tmp.contents[y : y + 3])
			disciplinas.append(disciplina)
			y += 3

		return curso


class AlunoHttp:
	def __init__(self, user, password):
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())

		urllib2.install_opener(self.opener)

		params = urllib.urlencode(dict(pr1 = user, pr2 = password))

		# Cria Cookie
		f = self.opener.open('https://webapp.pucrs.br/consulta/principal.jsp')
		f.close()

		# POST
		f = self.opener.open('https://webapp.pucrs.br/consulta/servlet/consulta.aluno.ValidaAluno', params)
		f.close()

	def getGrausinfo(self):
		# Pega os graus publicados
		f = self.opener.open('https://webapp.pucrs.br/consulta/servlet/consulta.aluno.Publicacoes')
		data = f.read()
		f.close()

		return data

def parse_pucrs(request, username, password):
	if username == None or password == None:
		html = "{\"error\":\"User or password is null\"}"
		return HttpResponse(html)

	try :
		# Log in :-)
		http_info = AlunoHttp(username, password)

		data = http_info.getGrausinfo()
		grausinfo = BeautifulSoup(data)

		s = grausinfo('div', {'id':'subtitulo'})
		# TODO: Verificar se o usuário foi bloqueado por excesso de tentativas com senha errada.
		if len(s) > 0 and "Acesso Negado" in s[0].text:
			ret = {}
			ret['error'] = "Acesso negado. Usuário ou senha inválidos."

			html = "%s" % simplejson.dumps(ret)
			return HttpResponse(html)

		aluno = Aluno()
		aluno.parseGrausData(grausinfo)

		html = "%s" % simplejson.dumps(aluno.info)
		return HttpResponse(html)
	except:
		return HttpResponse("{\"error\":\"Impossível acessar o servidor da PUCRS. Tente novamente mais tarde.\"}")

