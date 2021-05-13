from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer

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
				#query = Empleado.objects.filter(id_empleado=id_empleado_)
				return Response({'Error':'Por favor solo utilice números enteros positivos en id_empleado'})
			else:
				return Response({'Error':'Por favor solo utilice números enteros positivos en id_empleado'})
		elif 'edad' in keys:
			edad_ = request_dict['edad']
			'''
			if edad_.isnumeric():
				edad_ = str(edad_)
				query = Empleado.objects.filter(edad=edad_)
			'''
			if edad_.isalpha():
				query = Empleado.objects.filter(id_empleado=2)
				#query = Empleado.objects.filter(edad=edad_)
			else:
			
				return Response({'Error': 'Utilice números enteros y strings en el campo edad'})
		else:
			#Retorna una query correspondiente a un diccionario vacío 
			return Response({'':''})
		
		#Construye un serializer que se encargará de arreglar los queries 
		#en el formato adecuado para ser despachados 
		serializer = EmpleadoSerializer(query, many=True)
		data = serializer.data

		#Despacha la data en formato JSON
		if data:
			#Si alguna de las métricas fiscales es None, recalcula las métricas
						
			modelo_tributario = ModeloTributario()
			for i in range(len(data)):
				sal_libre_imp = data[i]['salario_libre_imp']
				imp = data[i]['impuestos']
				apt_seg_soc = data[i]['aportes_seg_soc']
				#if not sal_libre_imp or not imp or not apt_seg_soc:
				perfil = modelo_tributario.calcula_perfil_fiscal(data[i]['salario'])
					
				data[i]['salario_libre_imp'] = perfil[0]
				data[i]['impuestos'] = perfil[1]
				data[i]['aportes_seg_soc'] = perfil[2]
				data[i]['salario_neto'] = perfil[3]	
					
				
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

		if 'edad' in draft_request.keys():
			try:
				edad = draft_request['edad']
				edad = str(edad)
			except KeyError:
				return Response({"Error":"No pudo extraerse campo edad"})
		else:
			edad = None

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
			return Response(draft_request) 
		else:
			return Response(serializer.errors)


def error_404(request, exception):
	'''
	Clase para el manejo de la respuesta JSON a errores 4040
	'''
	#TODO:
		#1. Implementar apropiadamente con la clase exception_handler
	return JSONRenderer({"Error":"NotFound"})

