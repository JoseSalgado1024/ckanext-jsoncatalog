---

Requirimientos
---
 
 - Python 2.7
 - CKAN version: 2.5.2


Instalacion
---
Para la instalación de la extension  de CKAN, de realizar los siguientes pasos:

1. Activar el [virtualenv](https://wiki.archlinux.org/index.php/Python/Virtual_environment_(Espa%C3%B1ol)), Habitualmente, el virtualenv se ubica en:

        . /usr/lib/ckan/default/bin/activate


2. Instalar extension:

    - Mediante ``GITHUB``
    
            (pyenv)$ pip install -e "git+https://github.com/JoseSalgado1024/ckanext-jsoncatalog.git#egg=ckanext-jsoncatalog"


    - Instalar mediante ``PyPI``:

            (pyenv)$ pip install ckanext-jsoncatalog


3. Añadir ``jsoncatalog`` a la clausula ``ckan.plugins`` dentro del archivo de configuracion de ``CKAN``(Por omision es:``/etc/ckan/default/production.ini``).

        ckan.plugins = ... jsoncatalog 


4. Si deployaste ``CKAN`` usando WSGI y en ``Ubuntu``, deberias ejecutar:

        (pyenv)$ sudo service apache2 reload



Configurar
---

El plugin ``jsoncatalog`` posee algunas configuraciones que podes agregar a tu archivo de configuracion ``.ini`` para customizar la extension.

- Configurar endpoint de taxonomia de temas

        ckanext.json_catalog.uri = /themeTaxonomy.json


- Cambiar endpoint del catalogo

        ckanext.json_catalog.uri = /catalog.json

    
- Seleccionar un schema

        ckanext.jsoncatalog.schema = custom_schema


- Seleccionar una version diferente

        ckanext.jsoncatalog.schema_version = 1.0

Testing
---

        (pyenv)$ nosetests --nologcapture --with-pylons=test.ini

        (pyenv)$ nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.jsoncatalog --cover-inclusive --cover-erase --cover-tests
