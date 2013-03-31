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
 Haystack requiere :
 - Elasticsearch para soporte de la búsqueda (Requerido) Probado con la versión 0.19.9
 - RabbitMQ o REDIS para actualización en tiempo real de índice de búsqueda (Opcional)
   - RabbitMQ: $ apt-get install rabbitmq-server (Recomendado)
   - REDIS: $ apt-get install redis-server

  - Configurar en anunciaenradios/settings.py los datasources necesarios
