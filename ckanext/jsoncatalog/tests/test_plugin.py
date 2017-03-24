"""Tests for plugin.py."""
import ckanext.jsoncatalog.plugin as plugin
from ckanext.jsoncatalog.mappers import Mappers
from ckanext.jsoncatalog.formaters import WildCards
from ckan.config.environment import config
from ckanext.jsoncatalog.controller import JsonCatalogController
from ckan.tests import factories
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


def test_mappers_class_load_not_exists_schema():
    """
    Test 2: No existe schema provisto para carga de mappers.

    """
    mappers = Mappers()
    try:
        mappers.load(schema='no_existe', version='1.0')
    except IOError:
        pass


def test_mappers_class_load_not_exists_version():
    """
    Test 3: No existe version del schema provisto para carga de mappers.

    """
    mappers = Mappers()
    try:
        mappers.load(schema='default', version='no.existe')
    except IOError:
        pass


def test_mappers_class_init_cls_load_not_exists_version():
    """
    Test 4: No existe version del schema provisto para
    carga de mappers pero desde la creacion de la clase.

    """
    try:
        mappers = Mappers(schema='default', version='no.existe')
    except IOError:
        pass


@raises(IOError)
def test_mappers_class_int_cls_load_not_exists_schema():
    """
    Test 5: No existe schema provisto para carga de mappers
    pero desde la creacion de la clase.

    """
    mappers = Mappers()
    mappers.load(schema='no_existe', version='1.0')


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
    assert wildcards.apply('__@site_url__'), str


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
    print test_this
    print right_answers
    assert_equal(len(test_this), len(right_answers))


def test_wildcards_set_and_apply():
    """
    Test 9: Aplicar una wildcard a una frase.

    """
    wildcards = WildCards()
    for wildcard in wildcards.__dict__.keys():
        wildcards.__dict__[wildcard] = wildcard
    assert_equals(wildcards.apply('@site_url') == 'site_url', True)

"""

 Tests para clase Controller.

"""
