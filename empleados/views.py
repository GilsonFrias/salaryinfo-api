from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmpleadoSerializer
from .models import Empleado
from .tributaciones import ModeloTributario 
import sys

class HomeView(APIView):
	#Descripción para desplegar en HomeView:
	'''
	Salaryinfo-API
	REST API desarrollada en Django para la transacción de información financiera
	'''

	#HomeView es una subclase de la clase APIView, cuya misión es interconectar 
	#las URLs con los HTTP métodos siguiendo la architectura REST.

	# modelo_tributario contiene los métodos necesarios para el cálculo de perfiles fiscales
	modelo_tributario = ModeloTributario()

	def get(self, request):
		#Maneja los GET requests y suministra la respuesta HTTP apropiada

		#Extrae los argumentos recibidos 
		request_dict = request.query_params
		keys = request_dict.keys()
		
		#Extrae las filas apropiadas desde la base de datos de acuerdo a los 
		#pares key-value obtenidos en el método GET
		if 'lista' in keys:
			query = Empleado.objects.all()
		elif ('nombre' in keys) and ('apellido' in keys):
			nombre_ = request_dict['nombre']
			apellido_ = request_dict['apellido']
			if nombre_.isalpha() and apellido_.isalpha():
				query = Empleado.objects.filter(
						nombre=nombre_
					).filter(
						apellido=apellido_
					)
			else:
				return Response({'Error':'Por favor incluya solo carácteres alphabéticos en los campos nombre y apellido'})
		elif 'nombre' in keys:
			nombre_ = request_dict['nombre']
			if nombre_.isalpha():
				query = Empleado.objects.filter(nombre=nombre_)
			else:
				return Response({'Error':'Por favor incluya solo carácteres alphabéticos en el campo nombre'})
		elif 'apellido' in keys:
			apellido_ = request_dict['apellido']
			if apellido_.isalpha():
				query = Empleado.objects.filter(apellido=apellido_)
			else:
				return Response({'Error':'Por favor incluya solo carácteres alphabéticos en el campo apellido'})
		elif 'id_empleado' in keys:
			#Solamente carácteres numéricos pueden utilizarce como llaves de filtrado
			#para el campo id_empleado.
			id_empleado_ = request_dict['id_empleado']
			if id_empleado_.isnumeric():
				query = Empleado.objects.filter(id_empleado=id_empleado_)
			else:
				return Response({'Error':'Por favor solo utilice números enteros positivos en id_empleado'})
		else:
			#Retorna una query correspondiente a un diccionario vacío 
			return Response({'':''})
		
		#Construye un serializer que se encargará de arreglar los queries 
		#en el formato adecuado para ser despachados 
		serializer = EmpleadoSerializer(query, many=True)
		data = serializer.data

		#Despacha la data en formato JSON
		if data:
			return Response(data)
		else:
			return Response({'':''}) 

	def post(self, request):
		#El método post administra los POST requests y almacena nuevos datos en la base de datos

		#El objeto request es inmutable, copiémoslo para poder insertar las métricas fiscales
		draft_request = request.data.copy()
		
		#Verifica que los campos de nombre y apellido contengan solo carácteres alfabéticos
		if 'nombre' and 'apellido' in draft_request.keys():
			try:
				nombre = draft_request['nombre']
				apellido = draft_request['apellido']
				if (not nombre.isalpha() or not apellido.isalpha()) and (len(nombre)>0 and len(apellido)>0):
					return Response({'Error':'Por favor incluya solo carácteres alphabéticos en los campos nombre y apellido'}) 
			except KeyError:
				print('[Excepción] :: no pudo extraerse campo en POST request')
				return Response({'Error':'Parámetros (nombre, apellido) invalidos'})

		#Verifica si el salario fue pasado entre los pares key-value del POST request
		if 'salario' in draft_request.keys():
			modelo_tributario = ModeloTributario()
			try:
				#Calcula modelo tributario
				salario = draft_request['salario']
				#Elimina comas de la string 
				salario = salario.replace(',', '').strip()
				#Considera solo números positivos para el salario
				if not salario.isnumeric():
					return Response({'Error':'Por favor incluya solo números positivos y el punto decimal en el parámetro salario'}) 	
				draft_request['salario'] = salario
				perfil = modelo_tributario.calcula_perfil_fiscal(salario)
				#Si el valor retornado no es None, almacena las métricas calculadas en en objeto request
				if perfil:
					draft_request['salario_libre_imp'] = perfil[0]
					draft_request['impuestos'] = perfil[1]
					draft_request['aportes_seg_soc'] = perfil[2]
					draft_request['salario_neto'] = perfil[3]
				else:
					return Response({'Error':'Por favor incluya solo números positivos y el punto decimal en el parámetro salario'}) 	
			except KeyError:
				print('[Excepción] :: no pudo extraerse campo en POST request')
				return Response({'Error':'Parámetro (salario) inválido'})
		#Prepara los datos para ser almacenados en la base de datos
		serializer = EmpleadoSerializer(data=draft_request)
		if serializer.is_valid():
			#Si todos los campos cumplen con las condiciones de validez, almacénalos y emite 
			#un HTTP response con una representación JSON de los mismos.
			serializer.save()
			return Response(serializer.data) 
		else:
			return Response(serializer.errors)
