anunciaenradios
===============

Sistema E-Commerce de Anuncios en Radio

## Desarrollo
Recomendado usar virtualenvwrapper

- Instalación de dependencias:
 $ pip install -r requirements.txt
- Creación/Instalación del sistema base:
 $ python manage.py syncdb
- Iniciar el servidor de desarrollo:
 $ python manage.py runserver

## Servidores:  
 -Haystack requiere :
 	- Elasticsearch para soporte de la búsqueda (Requerido) Probado con la versión 0.19.9
 	- RabbitMQ o REDIS para actualización en tiempo real de índice de búsqueda (Opcional)
 		Instalción de los componentes:
   		- RabbitMQ: $ apt-get install rabbitmq-server (Recomendado)
   		- REDIS: $ apt-get install redis-server
   	** Para inciar el worker que se encarga de actualizar el índice en tiempo real ejecutar: $ ./start_worker
   	** En caso de que no se use un mecanismo para actualización en tiempo real del índice de forma periódica debe ejecutarse una tarea para con el comando $ python manage.py update_index para indexer todas las estaciones agregadas al sistema hasta ese momento.
   	** Si se tiene un índice sucio se puede recontruir usando: $ python manage.py rebuild_index
  - Configurar en anunciaenradios/settings.py los datasources necesarios
  - Configurar en anunciaenradios/settings.py el servidor de correo a utilizar
