#!/usr/bin/env python

from django.test import TestCase
from empleados.tributaciones import ModeloTributario
from empleados.models import Empleado

class EmpleadoTestCase(TestCase):

	'''
	Clase EmpleadosTestCase
	Esta clase contiene los unit test destinados a evaluar la funcionalidad de las clases ModeloTributario y Empleado. La clase ModeloTributario contiene los métodos necesarios para el cálculo del perfil fiscal de una entidad Empleado. La clase Empleado contiene las declaraciones de las especificaciones de los campos a almacenar en la base de datos al crear una entrada relacionada con un empleado en nómina.   
	''' 	
	def setUp(self):
		#Set up test objects
		self.modelo = ModeloTributario()
		self.empleado = Empleado.objects.create(
					nombre='Test', apellido='Subject', 
					salario=35000000.99, salario_libre_imp=10000000.00,
					impuestos=10000000.00, aportes_seg_soc=20000000.00,
					salario_neto=10000000.00
		) 	

	#1. Prueba los métodos específicos de la clase ModeloTributario
	def test_calcula_deducciones(self):
		#1. Pruebas con argumentos nulos
		salario = 0
		margenes = []
		tasas = []
	
		deducciones = self.modelo.calcula_deducciones(salario, margenes, tasas)
		self.assertEqual(deducciones, 0.0)

		#2. Pruebas con salario por debajo de todos los márgenes (sin deducciones)
		salario = 1000.05
		margenes = [2500.0, 3800.0, 7800.0]
		tasas = [0.11, 0.35, 0.45]

		deducciones = self.modelo.calcula_deducciones(salario, margenes, tasas)
		self.assertEqual(deducciones, 0.0)

		#3. Pruebas con salario por encima de todos los márgenes
		salario = 18000.0
		margenes = [7500.0, 10000.0, 15000.0]
		tasas = [0.10, 0.35, 0.40]

		deducciones = self.modelo.calcula_deducciones(salario, margenes, tasas)
		self.assertEqual(deducciones, 5050.0)

		#4. Pruebas con lista de margenes y tasas de descuentos no sorteadas
		salario = 18000.0
		margenes = [15000.0, 10000.0, 7500.0]
		tasas = [0.40, 0.35, 0.10]

		deducciones = self.modelo.calcula_deducciones(salario, margenes, tasas)
		self.assertEqual(deducciones, 5050.0)

	def test_calcula_perfil_fiscal(self):
		#1. Pruebas con salario sin valor numérico válido
		salario1 = '2*-.0'
		salario2 = 'c'
		salario3 = None

		perfil1 = self.modelo.calcula_perfil_fiscal(salario1)
		perfil2 = self.modelo.calcula_perfil_fiscal(salario2)
		perfil3 = self.modelo.calcula_perfil_fiscal(salario3)

		self.assertIsNone(perfil1)
		self.assertIsNone(perfil2)
		self.assertIsNone(perfil3)
	
		#2. Pruebas con salario por debajo de todos los márgenes (sin deducciones)
		salario = 8059.00
	
		perfil_fiscal = self.modelo.calcula_perfil_fiscal(salario)
		self.assertIsInstance(perfil_fiscal, tuple)
		self.assertEqual(perfil_fiscal[0], salario) #Prestaciones libres
		self.assertEqual(perfil_fiscal[1], 0.00)     #Impuestos
		self.assertEqual(perfil_fiscal[2], 0.00)     #Aportes Seg. Soc.
		self.assertEqual(perfil_fiscal[3], salario) #Salario neto

		#3. Pruebas con salario por encima de márgenes inferiores pero por debajo tope_exencion
		salario = 90000.00
	
		perfil_fiscal = self.modelo.calcula_perfil_fiscal(salario)
		self.assertIsInstance(perfil_fiscal, tuple)
		self.assertEqual(perfil_fiscal[0], 11000.00) #Prestaciones libres
		self.assertEqual(perfil_fiscal[1], 33800.00) #Impuestos
		self.assertEqual(perfil_fiscal[2], 10732.80) #Aportes Seg. Soc.
		self.assertEqual(perfil_fiscal[3], 45467.20) #Salario neto

		#4. Pruebas con salario por encima de tope_exencion (>USD 100,000)
		salario = 180000.00
	
		perfil_fiscal = self.modelo.calcula_perfil_fiscal(salario)
		self.assertIsInstance(perfil_fiscal, tuple)
		self.assertEqual(perfil_fiscal[0], 0.00)     #Prestaciones libres
		self.assertEqual(perfil_fiscal[1], 103500.00) #Impuestos
		self.assertEqual(perfil_fiscal[2], 36832.80) #Aportes Seg. Soc.
		self.assertEqual(perfil_fiscal[3], 39667.20) #Salario neto

	#2. Prueba la integridad de los campos del modelo Empleado al ser almacenados en la 
	#base de datos de prueba.
	def test_nombre_empleado(self):
		self.assertIsInstance(self.empleado.nombre, str)
		self.assertEqual(self.empleado.nombre, 'Test')
	
	def test_apellido_empleado(self):
		self.assertIsInstance(self.empleado.apellido, str)
		self.assertEqual(self.empleado.apellido, 'Subject')

	def test_salario_empleado(self):
		self.assertIsInstance(self.empleado.salario, float)
		self.assertEqual(self.empleado.salario, 35000000.99)

	def test_salario_libre_imp(self):
		self.assertIsInstance(self.empleado.salario_libre_imp, float)
		self.assertEqual(self.empleado.salario_libre_imp, 10000000.00)

	def test_aportes_seg_soc(self):
		self.assertIsInstance(self.empleado.aportes_seg_soc, float)
		self.assertEqual(self.empleado.aportes_seg_soc, 20000000.00)

	def test_salario_neto(self):
		self.assertIsInstance(self.empleado.salario_neto, float)
		self.assertEqual(self.empleado.salario_neto, 10000000.00)

