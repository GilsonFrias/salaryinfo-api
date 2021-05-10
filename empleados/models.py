from django.db import models
import datetime

#Create the 'empleados' object representation with Django's Object Relational Mapping 
'''
La clase Empleado contiene el modelo que será aplicado en la base de datos para definir, almacenar y recuperar los registros de empleados. 
'''
class Empleado(models.Model):
	id_empleado = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=15)
	apellido = models.CharField(max_length=15)
	salario = models.DecimalField(max_digits=10, decimal_places=2)
	salario_libre_imp = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	impuestos = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	aportes_seg_soc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	salario_neto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	def __str__(self):
		return f"{self.nombre} {self.apellido}"
