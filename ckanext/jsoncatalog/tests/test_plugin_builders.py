from nose.tools import *
from ckanext.jsoncatalog.builders import Catalog, ThemeTaxonomy, Dataset
import json


def test_create_catalog():
    """
    Test 1. builders.Catalog()
    Hipotesis: El metodo render() del catalogo, responde un diccionario.

    """
    catalog = Catalog()
    assert_equals(isinstance(catalog.render(), dict), True)


def test_create_catalog_is_json():
    """
    Test 2. builders.Catalog()
    Hipotesis: Al renderizar el catalogo, obtenemos un objeto JSON serializable.

    """
    catalog = Catalog()
    assert_equals(isinstance(json.dumps(catalog.render()), str), True)


def test_theme_taxonomy_a_list():
    """
    Test 3. builders.ThemeTaxonomy()
    Hipotesis: La Taxonomia de Temas es un Diccionario.

    """
    tt = ThemeTaxonomy()
    assert_equals(isinstance(tt.get_ckan_data(), list), True)


#def test_theme_taxonomy_render_is_a_dict():
#    """
#    Test 4: builders.ThemeTaxonomy()
#    Hipotesis: El metodo render() de ThemeTaxonomy, responde un diccionario
#
#    """
#    tt = ThemeTaxonomy()
#    print type(tt.render())
#    assert_equals(isinstance(tt.render(), dict), True)


def test_get_datasets_is_list():
    """
    Test 5. builders.Catalog()                                    |
    Hipotesis: TODO.                                              |
                                                                  |
    """
    dataset = Dataset()
    assert_equals(isinstance(dataset.get_ckan_data(), list), True)
