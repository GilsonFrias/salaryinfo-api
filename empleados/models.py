from django.db import models
import datetime

#Create the 'empleados' object representation with Django's Object Relational Mapping 
'''
La clase Empleado contiene el modelo que será aplicado en la base de datos para definir, almacenar y recuperar los registros de empleados. 

La tabla empleados_empleado contiene las entidades creadas de acuerdo al modelo Empleado, y la misma se encuentra en la base de datos SQLite del ubicada en el directorio raiz del proyecto.

A continuación se describen las sentencias para la creación de la tabla empleados_empleado:

CREATE TABLE IF NOT EXISTS "empleados_empleado" (
	"id_empleado" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"nombre" varchar(15) NOT NULL,
	"apellido" varchar(15) NOT NULL,
	"salario" decimal NOT NULL,
	"salario_libre_imp" decimal NULL,
	"impuestos" decimal NULL,
	"aportes_seg_soc" decimal NULL,
	"salario_neto" decimal NULL
);
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
