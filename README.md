## 1. Configuración

Despues de clonar el [repositorio](git@github.com:GilsonFrias/salaryinfo-api.git), utilice los siguientes comandos en Mac o Linux para instalar las dependencias necesarias y correr el servidor web:

```json
cd salaryinfo_api
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py runserver

```

Con el servidor en funcionamiento, visite la dirección http://127.0.0.1:8000/ en su navegador web para interactuar con la API. Adicionalmente, es recomendable utilizar el software [Postman](https://www.postman.com/product/api-client/)	 que facilita la emisión de request POST y GET y el monitoreo del comportamiento de la API. 


## 2. Comandos de interacción con la API


- Comandos GET para acceso a datos
	+ El argumento ```?lista``` insta a la API a retornar un listado de todos los empleados registrados en la base de datos. Ejemplo: http://127.0.0.1:8000/?lista.
	+ El argumento ```?nombre=``` pregunta a la API por todos los empleados con el mismo nombre. Por ejemplo, http://127.0.0.1:8000/?nombre=Nick.
	+ El argumento ```?apellido=``` todas las entradas en la base de datos con dicho apellido. Por ejemplo, http://127.0.0.1:8000/?apellido=Moreno.
	+ Combinando ambos argumentos ```?nombre``` y ```?apellido``` la API proporcionará los datos del empleado identificado como tal. Ejemplo, http://127.0.0.1:8000/?nombre=Maria&apellido=Moreno.
	+ Cada empleado es asignado un número entero único ```?id_empleado``` que también puede ser utilizado para obtener los datos del empleado: http://127.0.0.1:8000/?id_empleado=2.
	
- Comandos POST para escritura en database

	- Es posible el crear una nueva entrada en la database para un empleado al ejecutar un POST request pasando tres pares key-value: nombre, apellido y salario.
	- El valor del salario suministrado es luego utilizado en el cálculo del perfil fiscal del nuevo empleado. Dicho perfil está definido por 4 variables adicionales: salario-libre-imp, impuestos, aportes-seg-soc y salario-neto.

