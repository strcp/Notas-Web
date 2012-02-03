#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from M2Crypto import m2urllib2, SSL
import cookielib
import datetime

class Aluno:
	def __init__(self):
		self.info = {}

	def parseGrausData(self, soup, http_info):
		cursos = []

		if soup is None:
			return self.info

		tmp = soup.find('div', {'id':'header-print'})
		tmp1 = tmp.div.text.split('CGU:')
		nome = tmp1[0].split('Nome:')

		self.info['nome'] = nome[1]

		if soup is None:
			return curso

		tmp2 = soup.findAll("div", {"class":"tab_filter"})
		_cursos = tmp2[0].findAll("a")

		for c in _cursos:
			n = c.contents[0]
			n = n.strip()
			cursolink = 'https://memphis.ulbranet.com.br' + c['href']

			data = http_info.getDataFrom(cursolink)

			discSoup = BeautifulSoup(data)

			curso = self.createCurso(discSoup)
			curso['nome'] = n
			cursos.append(curso)

		self.info['cursos'] = cursos

		return self.info

	def createNota(self, tipo = None, valor = None):
		nota = {}

		nota['tipo'] = tipo
		nota['valor'] = valor

		return nota

	def createDisciplina(self, disciplina, final):
		disc = {}
		disc['nome'] = None
		disc['notas'] = None
		notas = []

		# TODO: Tratar erros
		if disciplina is None:
			return disc

		tmp = disciplina.find("div", {"class":"notas-disciplina"})
		disc['nome'] = tmp.text

		notas_parciais = disciplina.findAll("div", {"class":"notas-parciais"})

		for n in range(len(notas_parciais)):
			parcial = notas_parciais[n].contents
			tipo = parcial[0].strip()
			valor =  parcial[1].text
			nota = self.createNota(tipo, valor)
			notas.append(nota)

		if final is not None:
			final.text
			nota = self.createNota("Final", final.text)
			notas.append(nota)

		disc['notas'] = notas

		return disc

	def createCurso(self, soup):
		disciplinas = []
		curso = {}

		curso['disciplinas'] = disciplinas
		tmp1 = soup.findAll("li", {"id":"li_notas"})

		#print tmp1

		if len(tmp1) == 0:
			return curso

		# Verificamos se a última div de notas é referente ao semester atual ou
		# ao próximo
		today = datetime.date.today()
		for a in range(len(tmp1)):
			ano_semestre = tmp1[a].find("a", {"class":"link"})
			semestre = ano_semestre.text.split('/')

			if (int(semestre[1]) > 1) and (today.month >= 8):
				current = tmp1[0]
				break
			else:
				current = tmp1[1]
				break

		tmp = current.find("div", {"class":"notas-bloco"})  # Disciplinas do semestre corrente
		notas_finais = tmp.findAll("div", {"class":"notas-final"})
		discs = tmp.findAll("div", {"class":"notas-texto"})

		for t in range(len(discs)):
			if (len(notas_finais) >= t):
				final = notas_finais[t]
			else:
				final = None

			disciplina = self.createDisciplina(discs[t], final)
			disciplinas.append(disciplina)

		return curso

class AlunoHttp:
	txheaders = {
		'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
		'Accept-Language': 'en-us',
		'Accept-Encoding': 'gzip, deflate, compress;q=0.9',
		'Keep-Alive': '300',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
	}

	def __init__(self, user, password):

		ctx = SSL.Context('sslv3')

		self.params = urllib.urlencode(dict(i_Login = user, i_Senha = password))
		self.opener = m2urllib2.build_opener(ctx, urllib2.HTTPCookieProcessor())
		urllib2.install_opener(self.opener)

		# Cria Cookie
		f = self.opener.open('https://memphis.ulbranet.com.br/pls/ulbra24/AAmain.login', None, self.txheaders)
		f.close()

	def getDataFrom(self, link):
		if self.params is None:
			return None

		if link is None:
			return None

		f = self.opener.open(str(link), None, self.txheaders)

		data = f.read()
		f.close()

		return data

	def getGrausinfo(self):
		# Pega os graus publicados
		# POST
		if self.params is None:
			return None

		f = self.opener.open('https://memphis.ulbranet.com.br/pls/ulbra24/AAWEB.login', self.params, self.txheaders)
		f = self.opener.open('https://memphis.ulbranet.com.br/aa/notas', None, self.txheaders)

		data = f.read()
		f.close()

		return data

def parse_ulbra(request, username, password):
	if username == None or password == None:
		html = "{\"error\":\"User or password is null\"}"
		return HttpResponse(html)

	# Log in :-)
	try:
		http_info = AlunoHttp(username, password)

		data = http_info.getGrausinfo()
		grausinfo = BeautifulSoup(data)

		aluno = Aluno()
		try:
			aluno.parseGrausData(grausinfo, http_info)
			html = "%s" % simplejson.dumps(aluno.info)
		except:
			html = "{\"error\":\"Usuário ou senha inválidos.\"}"
		finally:
			return HttpResponse(html)
	except:
		html = "{\"error\":\"Erro conectando ao servidor da ULBRA.\"}"
		return HttpResponse(html)

