Salaryinfo-API sirve como una aplicación proof-of-concept para demostrar la versatilidad del framework de desarrollo web [Django](https://www.djangoproject.com/) y su paquete de extención para aplicaciones REST [Django REST](https://www.django-rest-framework.org/). 

La funcionalidad de la API se ha modelado para la acquisición y almacenamiento de datos concernientes a hojas de nómina, permitiendo a los consumidores de la API la utilización de métodos GET y POST para la interacción con una base de datos de prueba siguiendo la filosofía de la arquitectura REST. 


<div style="text-align:center">
    <img src='rsz_api.png', right=10></img>
</div>


___
## 1. Configuraciones para desplegar la aplicación

Las instrucciones siguientes están destindads a plataformas Mac y Linux, aunque el proceso de instalación de las dependencias y configuración del repositorio es bastante similar en Windows.

Serciorese de tenere Python3 instalado en su sistema, para comprobar que este es el caso, basta con abrir su terminal de comandos e introducir el comando ```Python3 -V```. La salida de la consola debe ser algo similar a ```Python 3.8.6```. De no ser así, visite la web oficial de [Python](https://www.python.org/downloads/) y siga las instrucciones para la instalación en su sistema operativo. 

Con Python instalado en su sistema, siga las siguientes instrucciones para configurar las dependencias y el repositorio:

- 1. Clone el rep el [repositorio](https://github.com/GilsonFrias/salaryinfo-api.git) para esto copie el comando siguiente y péguelo en su terminal de comandos:
    
```bash
git clone https://github.com/GilsonFrias/salaryinfo-api.git
```
	
- 2. Ingrese al directorio principal del repositorio utilizando el comando:
	
```bash
cd salaryinfo-api
```

- 3. Proceda a crear un medio virtual que servirá como una sandbox para contener las dependencias de Python necesarias:

```bash
python3 -m venv env
```
	
- 4. Si el comando anterior fue ejecutado sin complicaciones, deberá ahora de ser capaz de visualizar un nuevo directorio *env* en su directorio *salaryinfo-api*. Este es el directorio del medio virtual recién creado. Pase a activarlo utilizando el siguiente comando:

```bash
source env/bin/activate
```

- 5. Ahora pase a instalar las dependencias de Python necesarias, las mismas se encuentran registradas en el archivo requirements.txt. Utilizando pip en su consola de comandos, copie y pegue el comando:

```bash
pip install -r requirements.txt
```
    
- 6. Finalmente, inicialice el servidor de Django con el siguiente comando:

```bash
python manage.py runserver
```


Con el servidor en funcionamiento, visite la dirección [http://127.0.0.1:8000/](http://127.0.0.1:8000/) en su navegador web para interactuar con la API. Adicionalmente, es recomendable utilizar el software [Postman](https://www.postman.com/product/api-client/)	 que facilita la emisión de request POST y GET y el monitoreo del comportamiento de la API. 


## 2. Interactuando con la API

Las operaciones efectuadas con la API se realizan por HTTP. Los usuarios de la API deben utilizar métodos GET para el acceso a datos y métodos POST para la creación de nuevas entidades en la base de datos. Los verbos HTTP son siempre aplicados siguiendo la URL en la que está corriendo el servidor de Django, sin utilizar rutas intermedias. La siguiente tabla demuestra las diferentes funcionalidades de la API tomando en cuenta los diferentes parámetros HTTP necesarios para comunicarse de manera efectiva con la API. 


| Método HTTP/ Parámetro	| Acción             |	Example	       |Result  | 
| --------- | ------------------ | --------------- |------- |
| GET/ id_empleado	    | Retorna datos empleado con id_empleado | ?id_empleado=4	   | Retorna fila en base de datos indexada a id_empleados=4|
| GET/ nombre	| Retorna todas las instancias con nombre=nombre	 | ?nombre=Nick |Retorna todas las filas en la base de datos con el campo nombre=Nick|
| GET/ apellido	    | Retorna todas las instancias con apellido=apellido	     | ?apellido=Moreno   | Retorna todas las filas en la base de datos con el campo apellido=Moreno|
| GET/ lista	    | Retorna todos los elementos en bd	     | ?lista	   | retorna un listado de todos las filas en la base de datos|
| POST/ (nombre, apellido, salario)|Crea nueva entrada en base de datos |POST nombre=Manny, apellido=Nunez, salario=25700 |Crea nueva entrada en la base de datos y procede a la ejecución de código para el cálculo de prestaciones fiscales|

La respuesta de la API es siempre suministrada en formato JSON. El perfil fiscal asociado a una nueva entrada en la base de datos está definido por 4 variables calculadas con el salario bruto suministrado en el método POST: salario-libre-imp, impuestos, aportes-seg-soc y salario-neto. Dichas variables son asignadas a campos específicos dentro de la base de datos una vez creada la nueva entidad.
	


