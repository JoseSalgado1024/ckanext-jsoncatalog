# -*- coding: utf8 -*-
"""

"""
from ckanext.jsoncatalog.controller import *
logger = logging.getLogger('jsoncatalog')


class JsoncatalogPlugin(plugins.SingletonPlugin):
    """
    Implementación del plugin JSON Catalog plugin
    """
    plugins.implements(plugins.interfaces.IConfigurer)
    plugins.implements(plugins.interfaces.IRoutes, inherit=True)

    def update_config(self, config_):
        """
        Actualizar configuraciones, agregando las configuraciones del plugin.

        Args:
            - config_:
        Returns:
            - None
        """
        JsoncatalogPlugin.plugin_is_enable = config_.get("ckanext.json_catalog.is_active", "True") == 'True'
        JsoncatalogPlugin.catalog_url = config_.get("ckanext.json_catalog.uri", "/catalog.json")
        JsoncatalogPlugin.theme_taxonomy_url = config_.get("ckanext.json_catalog.uri", "/themeTaxonomy.json")
        toolkit.add_template_directory(config_, 'templates')

    def before_map(self, m):
        return m

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

