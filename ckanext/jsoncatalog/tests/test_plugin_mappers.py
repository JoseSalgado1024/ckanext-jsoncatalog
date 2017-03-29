"""Tests for plugin.py."""
import ckanext.jsoncatalog.plugin as plugin
from ckanext.jsoncatalog.mappers import Mappers
from ckanext.jsoncatalog.formaters import WildCards
from ckan.config.environment import config
# from ckanext.jsoncatalog.controller import JsonCatalogController
# from ckan.tests import factories
from os import path
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
    Test 7: Validar schema inexistente default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/no_existe_schema/1.0/{}.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), False)


def test_mappers_class_invalid_schema_version():
    """
    Test 8: Validar una version inexistente default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/default/no_existe/{}.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), False)


def test_mappers_class_invalid_mapper():
    """
    Test 9: Validar schema inexistente default.

    """
    mappers = Mappers()
    mappers.load(schema='default', version='1.0')
    plugin_path = path.dirname(__file__).replace('/tests', '')
    for mapper in mappers.__dict__.keys():
        mp = path.join(plugin_path, 'mappers/default/1.0/no_existe.json'.format(mapper))
        assert_equals(mappers.validate_mapper(mp), False)
