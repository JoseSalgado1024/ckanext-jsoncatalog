"""Tests for plugin.py."""
import ckanext.jsoncatalog.plugin as plugin
from ckanext.jsoncatalog.mappers import Mappers
from ckanext.jsoncatalog.formaters import WildCards
from ckan.config.environment import config
# from ckanext.jsoncatalog.controller import JsonCatalogController
# from ckan.tests import factories
from os import path
import ckan.model as model
from nose.tools import *


"""

 Tests para clase Mappers.

"""


def test_load_mappers():
    """
    Test 1: Carga de mappers por default.

    """
    mappers = Mappers()
    assert_equal(mappers.load(schema='default', version='1.0'), True)


@raises(IOError)
def test_mappers_class_load_not_exists_schema():
    """
    Test 2: No existe schema provisto para carga de mappers.

    """
    mappers = Mappers()
    mappers.load(schema='no_existe', version='1.0')


@raises(IOError)
def test_mappers_class_load_not_exists_version():
    """
    Test 3: No existe version del schema provisto para carga de mappers.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='no.existe')


@raises(IOError)
def test_mappers_class_init_cls_load_not_exists_version():
    """
    Test 4: No existe version del schema provisto para
    carga de mappers desde la creacion de la clase.

    """
    mappers = Mappers(schema='default', version='no.existe')


@raises(IOError)
def test_mappers_class_int_cls_load_not_exists_schema():
    """
    Test 5: No existe schema provisto para carga de mappers
    desde la creacion de la clase.

    """
    mappers = Mappers()
    mappers.load(schema='no_existe', version='1.0')


def test_mappers_class_valid_schema():
    """
    Test 6: Validar schemas default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/default/1.0/{}.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), True)


def test_mappers_class_invalid_schema():
    """
    Test 6: Validar schema inexistente default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/no_existe_schema/1.0/{}.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), False)


def test_mappers_class_invalid_schema_version():
    """
    Test 6: Validar una version inexistente default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/default/no_existe/{}.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), False)




def test_mappers_class_invalid_mapper():
    """
    Test 6: Validar schema inexistente default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/default/1.0/no_existe.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), False)


"""

 Tests para clase WindCards.

"""


def test_wildcards_class_instance():
    """
    Test 6: Crear una instancia de las clase WildCards
    """
    wildcards = WildCards()


def test_wildcards_apply_type():
    """
    Test 7: Aplicar una wildcard a una frase retorna una cadena.

    """
    wildcards = WildCards()
    print wildcards.apply('__@site_url__')
    print type(wildcards.apply('__@site_url__'))
    print isinstance(wildcards.apply('__@site_url__'), str)
    assert_equals(isinstance(wildcards.apply('__@site_url__'), (str, unicode)), True)


def test_wildcards_apply():
    """
    Test 8: Aplicar una wildcard a una frase.

    """
    wildcards = WildCards()
    right_answers = [{'site_url': config.get('ckan.site_url', 'http://127.0.0.1:5000')},
                     {'site_title': config.get('ckan.site_title', 'No definido')},
                     {'site_description': config.get('ckan.site_description', 'No definido')}]
    test_this = []
    for windc_name, windc_value in wildcards.__dict__.items():
        test_this.append({windc_name: windc_value})

    # Son iguales?
    assert_equal(len(test_this), len(right_answers))

    # Tienen los mismos valores?
    for tr in test_this:
        assert_equals(tr in right_answers, True)


def test_wildcards_set_and_apply():
    """
    Test 9: Aplicar un valor a una wildcard y luego aplicarlo a la frase.

    """
    wildcards = WildCards()
    for wildcard in wildcards.__dict__.keys():
        wildcards.__dict__[wildcard] = wildcard
    assert_equals(wildcards.apply('@site_url') == 'site_url', True)


def test_wildcards_list():
    """
    Test 10: Aplicar una wildcard a una frase retorna una cadena.

    """
    wildcards = WildCards()
    assert_equals(sorted(wildcards.list()), sorted(['site_url', 'site_description', 'site_title']))



"""

 Tests para clase Controller.

"""

"""

    Test Plugin.

"""


def test_plugin_load():
    """
    Test 11: Cargar el plugin.

    """
    plugin.plugins.load('jsoncatalog')
    #model.repo.rebuild_db()
