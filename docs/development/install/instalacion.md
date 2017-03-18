Instalacion:
---
Para la instalación de la extension  de CKAN, de realizar los siguientes pasos:

1. Activar el [virtualenv](https://wiki.archlinux.org/index.php/Python/Virtual_environment_(Espa%C3%B1ol)), for example::
     
```bash

# Habitualmente, el virtualenv se ubica aca
. /usr/lib/ckan/default/bin/activate

```

2. a. Instalar mediante ``github``:
```
(pyenv)$ pip install -e "git+https://github.com/JoseSalgado1024/ckanext-jsoncatalog.git#egg=ckanext-jsoncatalog"

```

2. b. Instalar mediante ``PyPI``:
```
(pyenv)$ pip install ckanext-jsoncatalog

```

3. Añadir ``jsoncatalog`` a la clausula ``ckan.plugins`` dentro del archivo de configuracion de ``CKAN``(Por omision es:``/etc/ckan/default/production.ini``).


4. Si deployaste ``CKAN`` usando WSGI y en ``Ubuntu``, deberias ejecutar:

```bash

sudo service apache2 reload

```
