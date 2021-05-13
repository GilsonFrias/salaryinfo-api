#!/usr/bin/env python
from rest_framework import serializers
from .models import Empleado

class EmpleadoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Empleado
		fields = [
			'id_empleado', 'nombre', 'apellido', 'salario',
			'salario_libre_imp', 'impuestos', 'aportes_seg_soc',
			'salario_neto', 'edad'
		]
