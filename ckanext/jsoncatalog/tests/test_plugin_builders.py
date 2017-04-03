# -*- coding: utf-8 -*-
"""

 Tests para clase Mappers.

"""
import nose.tools
from ckanext.jsoncatalog.builders import Catalog, ThemeTaxonomy, Dataset, Distribution
import json


def test_create_catalog():
    """
    Test 1. builders.Catalog()
    Hipotesis: El metodo render() del catalogo, responde un diccionario.

    """
    catalog = Catalog()
    nose.tools.assert_equals(isinstance(catalog.render(), dict), True)


def test_create_catalog_is_json():
    """
    Test 2. builders.Catalog()
    Hipotesis: Al renderizar el catalogo, obtenemos un objeto JSON serializable.

    """
    catalog = Catalog()
    nose.tools.assert_equals(isinstance(json.dumps(catalog.render()), str), True)


def test_theme_taxonomy_a_list():
    """
    Test 3. builders.ThemeTaxonomy()
    Hipotesis: La Taxonomia de Temas es un Diccionario.

    """
    tt = ThemeTaxonomy()
    nose.tools.assert_equals(isinstance(tt.get_ckan_data(), list), True)


def test_theme_taxonomy_is_json_serializable():
    """
    Test 4. builders.ThemeTaxonomy()
    Hipotesis: La Taxonomia de Temas es JSON serializable.

    """
    tt = ThemeTaxonomy()
    nose.tools.assert_equals(isinstance(json.dumps(tt.render()), str), True)


def test_get_datasets_is_a_list():
    """
    Test 5. builders.Dataset().
    Hipotesis: get_ckan_data() retorna una lista.

    """
    dataset = Dataset()
    nose.tools.assert_equals(isinstance(dataset.get_ckan_data(), list), True)


def test_get_datasets_json_serializable():
    """
    Test 6. builders.Dataset().
    Hipotesis: El metodo render() de la clase Dataset renderiza un objeto JSON serializable.

    """
    dataset = Dataset()
    nose.tools.assert_equals(isinstance(json.dumps(dataset.render()), str), True)


def test_get_distribution_is_a_list():
    """
    Test 7. builders.Dsitribution().
    Hipotesis: Dataset es una lista.

    """
    mock = []
    dist = Distribution(distribution=mock)
    nose.tools.assert_equals(isinstance(dist.get_ckan_data(), list), True)


def test_distribution_is_json_serializable():
    """
    Test 8. builders.Distribution().
    Hipotesis: El metodo render() de la clase Distribution renderiza un objeto JSON serializable.

    """
    mock = []
    dist = Distribution(distribution=mock)
    nose.tools.assert_equals(isinstance(json.dumps(dist.render()), str), True)
