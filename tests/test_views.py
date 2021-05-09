#!usr/bin/env python3
from django.test import TestCase

class TestHomeView(TestCase):

	'''
	Clase TestHomeView
	En esta clase se encuentran declarados todos los unit test destinados a probar la funcionalidad de la clase HomeView en el archivo views.py. La clase HomeView es la encargada de administrar los POST y GET requests suministrados a la API y de proporcionar la respuesta adecuada en cada caso. La clase django.test.Client utilizada aquí es capaz de generar los POST y GET requests especificados en la aplicación web sin la necesidad de correr el servidor web.

	'''
	#TODO:
		#1. Implementa los unit test para el método GET con solicitud
		#   simultánea de ?nombre y ?apellido
		#2. Declara los objetos de prueba en una única ocación como var. globales
		#3. Investiga cómo comunicarle a Django que no destruya las base de datos de prueba al pasar de unit test a unit test (utiliza una sola en lugar de crear varias)

	# 1. Prueba el método POST para la creación de una
	#entidad empleado en la base de datos de prueba

	#Prueba POST request a servidor sin argumentos
	def test_post_no_args(self):
		response = self.client.post('/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.content), 115) #size de error bytestring
	
	#Prueba POST con arg nombre solamente
	def test_post_nombre_only(self):
		response = self.client.post('/', {'nombre':'Bob'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.content), 78)

	#Prueba POST con arg apellido solamente
	def test_post_apellido_only(self):
		response = self.client.post('/', {'apellido':'Test'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.content), 52)
	
	#Prueba POST con arg salario solamente
	def test_post_salario_only(self):
		response = self.client.post('/', {'salario':'10000.00'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.content), 97)

	#Prueba POST con todos argumentos
	def test_post_valido(self):
		response = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		partial_response = b'{"id_empleado":1,'
		self.assertEqual(response.status_code, 200)
		#Confirma fue primera entidad creada en base datos
		self.assertEqual(response.content[:17], partial_response)


	# 2. Prueba de métodos GET

	#Prueba GET request a servidor sin parámetros
	def test_get_no_args(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b'{"":""}')

	#Prueba GET con argumento no reconocido por la API
	def test_get_bad_args(self):
		response = self.client.get('/?foo')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b'{"":""}')

	#Prueba GET request con argumento ?lista
	def test_get_lista(self):
		#Primero crea dos empleados en la base de datos
		_ = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		_ = self.client.post('/',
				{'nombre':'Alice', 
				'apellido':'Test', 
				'salario':'30000'}
		)
		#Solicita el listado de empleados y confirma que hay dos registros
		response = self.client.get('/?lista')
		contenido = str(response.content)
		numero_empleados = ['id_empleado' in term for term in contenido.split(',')]
		self.assertEqual(response.status_code, 200)
		self.assertEqual(sum(numero_empleados), 2)

	#Prueba de solicitud de id_empleado con argumento inválido (carácteres no numéricos)
	def test_get_id_bad_args(self):
		response = self.client.get('/?id_empleado=a#%8')
		#Confirma que mensaje JSON de error fue suministrado {"Error":"Por favor...}'
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content[1:8], b'"Error"')

	#Prueba de solicitud de id_empleado con argumento válido
	def test_get_id_good_args(self):
		_ = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		response = self.client.get('/?id_empleado=1')
		contenido = str(response.content).split(',')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(contenido[0][4:], '"id_empleado":1')
		self.assertEqual(contenido[1], '"nombre":"Bob"')


	#Prueba método GET con nombre inválido carácteres no alfabéticos presentes
	def test_get_nombre_bad_args(self):
		_ = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		response = self.client.get('/?nombre=$9.0.5%foo')
		#Confirma que mensaje JSON de error fue suministrado {"Error":"Por favor...}'
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content[1:8], b'"Error"')
	
	#Prueba GET con nombre válido (carácteres alfabéticos solamente) pero no presente en base de datos:	
	def test_get_nombre_not_in_db(self):
		_ = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		response = self.client.get('/?nombre=foo')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b'{"":""}')

	#Prueba GET con nombre válido (carácteres alfabéticos solamente) presente en base de datos:	
	def test_get_nombre_in_db(self):
		_ = self.client.post('/',
				{'nombre':'Alice', 
				'apellido':'Test', 
				'salario':'25000'}
		)
		response = self.client.get('/?nombre=Alice')
		contenido = str(response.content).split(',')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(contenido[0][4:], '"id_empleado":1')
		self.assertEqual(contenido[1], '"nombre":"Alice"')

	#Prueba método GET con apellidoe inválido (carácteres no alfabéticos presentes)
	def test_get_apellido_bad_args(self):
		_ = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		response = self.client.get('/?apellido=$9.0.5%foo')
		#Confirma que mensaje JSON de error fue suministrado {"Error":"Por favor...}'
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content[1:8], b'"Error"')
	
	#Prueba GET con apellido válido (carácteres alfabéticos solamente) pero no presente en base de datos:	
	def test_get_apellido_not_in_db(self):
		_ = self.client.post('/',
				{'nombre':'Bob', 
				'apellido':'Test', 
				'salario':'10000'}
		)
		response = self.client.get('/?apellido=foo')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b'{"":""}')

	#Prueba GET con apellido válido (carácteres alfabéticos solamente) presente en base de datos:	
	def test_get_nombre_in_db(self):
		_ = self.client.post('/',
				{'nombre':'Alice', 
				'apellido':'Test', 
				'salario':'25000'}
		)
		response = self.client.get('/?apellido=Test')
		contenido = str(response.content).split(',')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(contenido[0][4:], '"id_empleado":1')
		self.assertEqual(contenido[1], '"nombre":"Alice"')
