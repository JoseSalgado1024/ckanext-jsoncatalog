"""

 Tests para clase Wildcards.

"""
from ckanext.jsoncatalog.formaters import WildCards
from nose.tools import *
from ckan.config.environment import config


def test_wildcards_class_instance():
    """
    Test 10:
    Hipotesis: Crear una instancia de las clase WildCards
    """
    wildcards = WildCards()
    wildcards.list()


def test_wildcards_apply_type():
    """
    Test 11: Aplicar una wildcard a una frase retorna una cadena.

    """
    wildcards = WildCards()
    assert_equals(isinstance(wildcards.apply('__@site_url__'), (str, unicode)), True)


def test_wildcards_apply():
    """
    Test 12: Aplicar una wildcard a una frase.

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
    Test 13: Aplicar un valor a una wildcard y luego aplicarlo a la frase.

    """
    wildcards = WildCards()
    for wildcard in wildcards.__dict__.keys():
        wildcards.__dict__[wildcard] = wildcard
    assert_equals(wildcards.apply('@site_url') == 'site_url', True)


def test_wildcards_list():
    """
    Test 14: Aplicar una wildcard a una frase retorna una cadena.

    """
    wildcards = WildCards()
    assert_equals(sorted(wildcards.list()), sorted(['site_url', 'site_description', 'site_title']))
