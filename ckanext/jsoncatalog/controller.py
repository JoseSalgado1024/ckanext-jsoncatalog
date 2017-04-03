import ckan.plugins as plugins
from pylons import response
from ckan.lib.base import BaseController
from ckan.config.environment import config as ckan_config
from mappers import *
from builders import Catalog, ThemeTaxonomy

logger = logging.getLogger('jsoncatalog.controller')


class JsonCatalogController(BaseController):
    """
    Controlador principal del plugin.
    """
    _errors_json = []

    def __init__(self):
        plugin_folder = path.dirname(__file__)
        self.mappers_folder = path.join(plugin_folder, 'mappers')

        self.mapper_name = ckan_config.get('ckanext.json_catalog.schema', 'default')
        self.mapper_version = ckan_config.get('ckanext.json_catalog.version', '1.0')

    def generate_catalog(self):
        """
        Genera catalogo.json.

        La generacion del catalogo se realiza mediante el uso de los field
        propios de las datasets almacenados en CKAN y las reglas de mapeo
        definidas en el mapper.

        Args:
            - None.

        Returns:
            - JSON response. Catalogo en formato json.
        """
        err_response = {
            'status': 404,
            'message': ''
        }
        try:
            my_catalog = Catalog(mapper=self.mapper_name, version=self.mapper_version)
            return self.build_response(my_catalog.render())
        except KeyError:
            err_response.update({'message': 'Faltan Parametros requerido.'})
        except ValueError:
            err_response.update({'message': 'Formato no esperado.'})
        return self.build_response(err_response)

    def generate_theme_taxonomy(self):
        """
        Genera la taxonomia de temas.

        Args:
            - None.

        Returns:
            - JSON response. ThemeTaxonomy en formato json.
        """
        _response = {
            'status': 404,
            'message': ''
        }
        thm_txnm = []
        try:
            thm_txnm = ThemeTaxonomy()
            return self.build_response(thm_txnm.render())
        except KeyError as e:
            _response['message'] = 'Falta parametro {} requerido.'.format(e)
        except ValueError as e:
            _response['message'] = 'La clave {} no existe dentro de CKAN.'.format(e)
        finally:
            if len(_response['message']) < 0:
                _response = thm_txnm
        return self.build_response(_response)

    @staticmethod
    def build_response(_json_data):
        data = {}
        if isinstance(_json_data, (dict, list)):
            data = _json_data
        response.content_type = 'application/json; charset=UTF-8'
        del response.headers["Cache-Control"]
        del response.headers["Pragma"]
        return plugins.toolkit.literal(json.dumps(data))

