# coding: utf8
"""

"""
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from pylons import response
from ckan.lib.base import BaseController
import json
import logging
from os import path
from controller import *
logger = logging.getLogger('jsoncatalog')


class JsoncatalogPlugin(plugins.SingletonPlugin):
    """

    """
    plugins.implements(plugins.interfaces.IConfigurer)
    plugins.implements(plugins.interfaces.IRoutes, inherit=True)

    def update_config(self, config_):
        """

        Args:
            - config_:
        Returns:
            - None
        """
        JsoncatalogPlugin.plugin_is_enable = config_.get("ckanext.json_catalog.is_active", "True") == 'True'
        JsoncatalogPlugin.catalog_url = config_.get("ckanext.json_catalog.uri", "/catalog.json")
        JsoncatalogPlugin.mapper_version = config_.get("ckanext.json_catalog.mapper_version", "1.0")
        JsoncatalogPlugin.theme_taxonomy_url = config_.get("ckanext.json_catalog.uri", "/themeTaxonomy.json")
        plugin_folder = path.dirname(__file__)
        JsoncatalogPlugin.mappers_folder = path.join(plugin_folder, 'mappers')
        toolkit.add_template_directory(config_, 'templates')

    def before_map(self, m):
        return m

    def load_mapper(self):
        """

        :return:
        """
        pass

    def after_map(self, m):
        if JsoncatalogPlugin.plugin_is_enable:
            m.connect('write_catalog',
                      JsoncatalogPlugin.catalog_url,
                      controller='ckanext.jsoncatalog.plugin:JsonCatalogController',
                      action='generate_catalog')
            m.connect('write_theme_taxonomy',
                      JsoncatalogPlugin.theme_taxonomy_url,
                      controller='ckanext.jsoncatalog.plugin:JsonCatalogController',
                      action='generate_theme_taxonomy')
            return m

