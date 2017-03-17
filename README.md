<!-- ••• -->
[![Build Status](https://travis-ci.org/JoseSalgado1024/ckanext-jsoncatalog.svg?branch=master)](https://travis-ci.org/JoseSalgado1024/ckanext-jsoncatalog)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/358fea95190c4f068492b66390b3a3de)](https://www.codacy.com/app/JoseSalgado1024/ckanext-jsoncatalog?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JoseSalgado1024/ckanext-jsoncatalog&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/JoseSalgado1024/ckanext-jsoncatalog/badge.svg?branch=master)](https://coveralls.io/github/JoseSalgado1024/ckanext-jsoncatalog?branch=master)
[![Coverage Status](https://img.shields.io/github/license/mashape/apistatus.svg)](https://img.shields.io/github/license/mashape/apistatus.svg)
[![Code Climate](https://codeclimate.com/github/JoseSalgado1024/ckanext-jsoncatalog/badges/gpa.svg)](https://codeclimate.com/github/JoseSalgado1024/ckanext-jsoncatalog)
[![Issue Count](https://codeclimate.com/github/JoseSalgado1024/ckanext-jsoncatalog/badges/issue_count.svg)](https://codeclimate.com/github/JoseSalgado1024/ckanext-jsoncatalog)


ckanext-jsoncatalog
---

Indice:
---

<!-- MarkdownTOC -->

- [Requirimientos:](#requirimientos)
- [Instalacion:](#instalacion)
- [Configurar:](#configurar)
- [Development Installation](#development-installation)
- [Running the Tests](#running-the-tests)

<!-- /MarkdownTOC -->


Requirimientos:
---
CKAN version: 2.5.2


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


Configurar:
---

El plugin ``jsoncatalog`` posee algunas configuraciones que podes agregar a tu archivo de configuracion ``.ini`` para customizar la extension.


### Selecion de un Schema diferente de catalogo:
```bash
    ckanext.jsoncatalog.schema = some_default_value
```



To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.jsoncatalog --cover-inclusive --cover-erase --cover-tests