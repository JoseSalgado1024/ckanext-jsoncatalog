import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from pylons import response
from ckan.lib.base import BaseController
from ckan.config.environment import config as ckan_config
from mappers import *


logger = logging.getLogger('jsoncatalog.controller')


class JsonCatalogController(BaseController):
    """
    Controlador principal del plugin.
    """
    _errors_json = []

    def __init__(self):
        plugin_folder = path.dirname(__file__)
        self.mappers_folder = path.join(plugin_folder, 'mappers')

        mapper = ckan_config.get('ckanext.json_catalog.schema', 'default')
        mapper_version = ckan_config.get('ckanext.json_catalog.version', '1.0')

        self.mappers = Mappers(schema=mapper, version=mapper_version)
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
            thm_txnm = self.map_themes(self.get_themes())
            return self.build_response(thm_txnm)
        except KeyError as e:
            _response['message'] = 'Falta parametro {} requerido.'.format(e)
        except ValueError, e:
            _response['message'] = 'La clave {} no existe dentro de CKAN.'.format(e)
        finally:
            if len(_response['message']) < 0:
                _response = thm_txnm
        return self.build_response(_response)

    def get_catalog(self):
        """
        Obtiene informacion del catalogo.

        Retunrs:
            - Dict.
        """

        return self.get_ckan_data(_content_of='catalog')

    def map_catalog(self, _catalog):
        """

        Returns:
            Dict():
                - {}(vacio), ante Fallo.
                - {catalogo}, Exito.

        """
        mapped_catalogs = {}
        try:
            mapped_catalogs = self.mappers.apply(data=_catalog, _mapper='catalog')
            for k, v in mapped_catalogs.items():
                if u'@datasets' == unicode(v):
                    mapped_catalogs.update({k: self.map_dataset(self.get_datasets())})
                if u'@themeTaxonomy' == unicode(v):
                    mapped_catalogs.update({k: self.map_themes(self.get_themes())})
        except (AttributeError, TypeError, KeyError) as e:
            logger.error('>> {}'.format(e))
        return mapped_catalogs

    @staticmethod
    def get_ckan_data(_content_of='catalog', id=None):

        if _content_of.lower() == 'catalog':
            datadict = {'sort': 'metadata_modified desc',
                        'rows': 5000}
            action = u'package_search'
            return toolkit.get_action(action)(data_dict=datadict)
        elif _content_of.lower() == 'distributions':
            datadict = {'sort': 'metadata_modified desc',
                        'rows': 5000}
            action = u'package_search'
            return toolkit.get_action(action)(data_dict=datadict)['results']
        elif _content_of.lower() == 'datasets':
            datadict = {'sort': 'metadata_modified desc',
                        'id': '',
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
                    if u'@distributions' == unicode(v):
                        mapped_dataset.update({k: self.map_distribution(self.get_themes())})
        except (AttributeError, TypeError, KeyError),  e:
            logger.error('++ {}'.format(e))
        return mapped_datasets

    def exists(self, _obj='dataset', _key=None, _value=None):
        """
        Busqueda dentro de la data de ckan.

        Args:
            - _obj:
            - key_to_search:

        Returns:
             - bool():
                - True, Existe dentro de _obj la clave:_key y posee el valor: _value.
                - False: No existe dentro de _obj la clave:_key o no posee el valor: _value.
        """
        def search_in_dict(d, _k, _v):
            r = False
            try:
                if d[_k] == _v:
                    r = True
            except IndexError:
                pass
            return r

        # si _key o _value es None, retorno false.
        results = False
        if None in [_key, _value]:
            return results
        data = self.get_ckan_data(_obj)
        if isinstance(data, list):
            for elem in data:
                results = search_in_dict(elem, _key, _value)
                if results:
                    break
        elif isinstance(data, dict):
            results = search_in_dict(data, _key, _value)
        else:
            return results
        return results

    def map_distribution(self, _dataset):
        mapped_distributions = []
        try:
            mapped_distributions = self.mappers.apply(_dataset, _mapper='distributions')
        except (AttributeError, TypeError, KeyError), e:
            logger.error('[mapper.distributions] {}'.format(e))
        return mapped_distributions

    def get_dataset(self, dataset_id=None):
        """
        Obtener diccionario con el contenido del dataset.

        Returns:
          - dict(). Len(dict) == n: Lista de los n grupos existentes en CKAN.
          - dict(). Len(dict) == 0: si ocurrio un error o no se han cargado dataset.
        """
        _dataset = {}
        if dataset_id in [None]:
            return _dataset
        return self.get_ckan_data(_content_of='distributions')

    def map_themes(self, _themes):
        mapped_themes = []
        try:
            mapped_themes = self.mappers.apply(_themes, _mapper='themeTaxonomy')
        except (AttributeError, TypeError, KeyError) as e:
            logger.error('-- {}'.format(e))

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
