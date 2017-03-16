import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from pylons import response
from ckan.lib.base import BaseController
from mappers import *
logger = logging.getLogger('jsoncatalog.controller')


class JsonCatalogController(BaseController):
    """
    Controlador principal del plugin.
    """
    _errors_json = []

    def __init__(self):
        self.mappers = Mappers()
        self.wildcards = WildCards()

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
            return self.build_response(self.map_catalog(self.get_catalog()))
        except KeyError:
            return self.build_response(err_response.update({'message': 'Faltan Parametros requerido.'}))
        except ValueError:
            return self.build_response(err_response.update({'message': 'Formato no esperado.'}))

    def generate_theme_taxonomy(self):
        """
        Genera la taxonomia de temas.

        Args:
            - None.

        Returns:
            - JSON response. ThemeTaxonomy en formato json.
        """
        err_response = {
            'status': 404,
            'message': ''
        }
        try:
            thm_txnm = self.map_themes(self.get_themes())
            return self.build_response(thm_txnm)
        except KeyError, e:
            err_response['message'] = 'Falta parametro {} requerido.'.format(e)
            return self.build_response(err_response)
        except ValueError, e:
            err_response['message'] = 'La clave {} no existe dentro de CKAN.'.format(e)
            return self.build_response(err_response)

    def get_catalog(self):
        """
        Obtiene informacion del catalogo.

        Retunrs:
            - TODO.
        """

        return self.get_ckan_data(_content_of='catalog')

    def map_catalog(self, _catalog):
        """

        :return:
        """
        mapped_catalogs = {}
        try:
            mapped_catalogs = self.mappers.apply(_catalog, _mapper='catalog')
            for k, v in mapped_catalogs.items():
                if u'@datasets' == unicode(v):
                    mapped_catalogs.update({k: self.map_dataset(self.get_datasets())})
                if u'@themeTaxonomy' == unicode(v):
                    mapped_catalogs.update({k: self.map_themes(self.get_themes())})
        except (AttributeError, TypeError, KeyError), e:
            print e
            # log entry
            pass
        return mapped_catalogs

    @staticmethod
    def get_ckan_data(_content_of='catalog'):
        if _content_of.lower() == 'catalog':
            datadict = {'sort': 'metadata_modified desc',
                        'rows': 5000}
            action = u'package_search'
            return toolkit.get_action(action)(data_dict=datadict)
        elif _content_of.lower() == 'datasets':
            datadict = {'sort': 'metadata_modified desc',
                        'rows': 5000}
            action = u'package_search'
            return toolkit.get_action(action)(data_dict=datadict)['results']
        elif _content_of.lower() == 'groups':
            datadict = {'all_fields': True}
            action = u'group_list'
            return toolkit.get_action(action)(data_dict=datadict)
        else:
            raise AttributeError

    def get_datasets(self):
        """
        Obtener lista de datasets contenidos dentro de CKAN.

        Returns:
            - List(). Len(list) == n: Lista de los n Dataset existentes en CKAN.
            - List(). Len(list) == 0: si ocurrio un error o no se han cargado datasets.
        """
        return self.get_ckan_data(_content_of='datasets')

    def map_dataset(self, _datasets):
        mapped_datasets = []
        try:
            mapped_datasets = self.mappers.apply(_datasets, _mapper='dataset')
            for mapped_dataset in mapped_datasets:
                for k, v in mapped_dataset.items():
                    if u'@distribution' == unicode(v):
                        mapped_dataset.update({k: self.map_themes(self.get_themes())})
        except (AttributeError, TypeError, KeyError), e:
            print e
            # log entry
            pass
        return mapped_datasets

    def get_themes(self):
        return self.get_ckan_data(_content_of='groups')

    def map_themes(self, _themes):
        mapped_themes = []
        try:
            mapped_themes = self.mappers.apply(_themes, _mapper='themeTaxonomy')
        except (AttributeError, TypeError, KeyError), e:
            print e
            # log entry
        return mapped_themes

    @staticmethod
    def build_response(_json_data):
        data = {}
        if isinstance(_json_data, (dict, list)):
            data = _json_data
        response.content_type = 'application/json; charset=UTF-8'
        del response.headers["Cache-Control"]
        del response.headers["Pragma"]
        return plugins.toolkit.literal(json.dumps(data))
