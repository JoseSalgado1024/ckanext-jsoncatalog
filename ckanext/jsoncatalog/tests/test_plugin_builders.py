from nose.tools import *
from ckanext.jsoncatalog.builders import Catalog
import json


def test_create_catalog():
    """
    Test 1. builders.Catalog()
    Hipotesis: TODO.

    """
    catalog = Catalog()
    assert_equals(isinstance(catalog.render(), str), True)


def test_create_catalog_is_json():
    """
    Test 2. builders.Catalog()
    Hipotesis: TODO.

    """
    catalog = Catalog()
    assert_equals(isinstance(json.dumps(catalog.render()), str), True)


def test_get_groups_is_list():
    """
    Test 3. builders.Catalog()
    Hipotesis: TODO.

    """
    catalog = Catalog()
    print 'get groups'
    print type(catalog.get_ckan_data('groups'))
    print catalog.get_ckan_data('groups')
    assert_equals(isinstance(catalog.get_ckan_data('groups'), list), True)


def test_get_datasets_is_list():
    """
    Test 4. builders.Catalog()
    Hipotesis: TODO.

    """
    catalog = Catalog()
    assert_equals(isinstance(catalog.get_ckan_data('datasets'), list), True)
