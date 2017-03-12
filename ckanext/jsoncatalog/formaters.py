from os import environ
import ckan.model as model
from ckan.config.environment import config


class Utiles(object):
    host = config.get('ckan.site_url')