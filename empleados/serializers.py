#!/usr/bin/env python
from rest_framework import serializers
from .models import Empleado

'''
class EmpleadoSerializer(serializers.Serializer):
	id_empleado = serializers.IntegerField(read_only=True)
	nombre = serializers.CharField(max_length=15)
	apellido = serializers.CharField(max_length=15)
	salario = serializers.DecimalField(decimal_places=2, max_digits=10)
	salario_libre_imp = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=10, required=False)
	impuestos = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=10, required=False)
	aportes_seg_soc = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=10, required=False)
	salario_neto = serializers.DecimalField(allow_null=True, decimal_places=2, max_digits=10, required=False)
	edad = serializers.CharField(required=False, allow_null=True, max_length=3)

	def create(self, validated_data):
		return Empleado.objects.create(**validated_data)


	def update(self, instance, validated_data):
		instance.id_empleado = validated_data.get('id_empleado', instance.id_empleado)
		instance.nombre = validated_data.get('nombre', instance.nombre)
		instance.apellido = validated_data.get('salario_libre_imp', instance.salario_libre_imp)
		instance.impuestos = validated_data.get('impuestos', instance.impuestos)
		instance.aportes_seg_soc = validated_data.get('aportes_seg_soc', instance.aportes_seg_soc)
		instance.salario_neto = validated_data.get('salario_neto', instance.salario_neto)
		instance.edad = validated_data.get('edad', instance.edad) 
		instance.save()
		return instance

'''
class EmpleadoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Empleado
		fields = '__all__'

		#fields = ('id_empleado', 'impuestos', 'salario_neto')
		#fields = [
		#	'id_empleado', 'nombre', 'apellido', 'salario',
#			'salario_libre_imp', 'impuestos', 'aportes_seg_soc',
#			'salario_neto', 'edad'
#		]
