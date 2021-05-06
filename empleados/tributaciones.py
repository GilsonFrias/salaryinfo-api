#!/usr/bin/env python

'''
'''
import json
import os

class ModeloTributario(object):

	def __init__(self):
		directorio = os.path.dirname(os.path.realpath(__file__))
		directorio = os.path.join(directorio, 'parametros_tributarios.json')
		self.contenido_json = self.carga_JSON(directorio)
		
		self.margenes_imp = self.contenido_json['margenes-imp']
		self.tasas_imp= self.contenido_json['tasas-imp']
		self.margenes_ss = self.contenido_json['margenes-ss']
		self.tasas_ss = self.contenido_json['tasas-ss']
		self.tope_exencion = self.contenido_json['tope-exencion']

	def calcula_perfil_fiscal(self, salario):
		try:
			salario = float(salario)
		except ValueError:
			print('[Excepción] :: argumento sin representación numérica pasado a método calcula_prestaciones')
			return None
		except TypeError:
			print('[Excepción] :: argumento pasado a método calcula_prestaciones debe ser númbero o string')
			return None
			
		impuestos = 0.0
		aportes_ss = 0.0
		prestacion_libre = min(self.margenes_imp[0], salario)
		salario_neto = 0.0
		
		#1. Cálculo impuestos
		impuestos += self.calcula_deducciones(salario, self.margenes_imp[1:], self.tasas_imp[1:])
			#Ajusta margen mínimo de exención de impuestos si salario > USD 100,000
		if salario > self.tope_exencion:
			prestacion_libre -= (salario-self.tope_exencion)//2
			prestacion_libre = max(prestacion_libre, 0.0)
		
		impuestos += self.calcula_deducciones(salario, [prestacion_libre], [self.tasas_imp[0]])
 
		#2. Cálculo cotizaciones seguridad social
		aportes_ss += self.calcula_deducciones(salario, self.margenes_ss, self.tasas_ss)
		
		#3. Cálculo salario neto despues de deducciones
		salario_neto = salario - impuestos - aportes_ss

		#Keep all numbers with a precision of 2 decimal points
		prestacion_libre = round(prestacion_libre, 2)
		impuestos = round(impuestos, 2)
		aportes_ss = round(aportes_ss, 2)
		salario_neto = round(salario_neto, 2)

		return (prestacion_libre, impuestos, aportes_ss, salario_neto)

	def calcula_deducciones(self, salario, margenes, tasas):
		n = len(margenes)
		deducciones = 0.0
		for i in range(n, 0, -1):
			margen = margenes[i-1]
			if salario > margen:
				gravamen = tasas[i-1] 
				deducciones += (salario-margen)*gravamen
		return deducciones
		

	def carga_JSON(self, filename):
		'''
		Lee un archivo JSON desde el directorio definido en filename
		'''
		try:
			with open(filename, 'r', encoding='utf-8-sig') as archivo_json:
				data = json.load(archivo_json)
				return data
		except FileNotFoundError:
			print('[Excepción] :: archivo no encontrado en carga_JSON')
			return None
