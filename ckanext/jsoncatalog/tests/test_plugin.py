"""

    Test Plugin.

"""
import ckanext.jsoncatalog.plugin as plugin
# from ckanext.jsoncatalog.formaters import WildCards
# from ckan.config.environment import config
# from nose.tools import *


def test_plugin_load():
    """
    Test 11: Cargar el plugin.

    """
    plugin.plugins.unload('jsoncatalog')

