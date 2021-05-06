## 1. Configuración

Las instrucciones siguientes están destindads a plataformas Mac y Linux, aunque el proceso de instalación de las dependencias y configuración del repositorio es bastante similar en Windows.

Serciorese de tenere Python3 instalado en su sistema, para comprobar que este es el caso, basta con abrir su terminal de comandos e introducir el comando ```Python3 -V```. La salida de la consola debe ser algo similar a ``Python 3.8.6```. De no ser así, visite la web oficial de [Python](https://www.python.org/downloads/) y siga las instrucciones para la instalación en su sistema operativo. 

Con Python instalado en su sistema, siga las siguientes instrucciones para configurar las dependencias y el repositorio:

- 1. Clone el rep el [repositorio](git@github.com:GilsonFrias/salaryinfo-api.git) para esto copie el comando siguiente y péguelo en su terminal de comandos:

	```git clone git@github.com:GilsonFrias/salaryinfo-api.git```
	
- 2. Ingrese al directorio principal del repositorio utilizando el comando:
	
	```cd salaryinfo-api```

- 3. Proceda a crear un medio virtual que servirá como una sandbox para contener las dependencias de Python necesarias:

	```python3 -m venv env``
	
- 4. Si el comando anterior fue ejecutado sin complicaciones, deberá ahora de ser capaz de visualizar un nuevo directorio *env* en su directorio *salaryinfo-api*. Este es el directorio del medio virtual recién creado. Pase a activarlo utilizando el siguiente comando:

	```source env/bin/activate```

- 5. Ahora pase a instalar las dependencias de Python necesarias, las mismas se encuentran registradas en el archivo requirements.txt. Utilizando pip en su consola de comandos, copie y pegue el comando:

	```pip install -r requirements.txt``

- 6. Finalmente, inicialice el servidor de Django con el siguiente comando:

	```python manage.py runserver```

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

