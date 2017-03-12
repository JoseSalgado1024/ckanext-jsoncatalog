import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from pylons import response
from ckan.lib.base import BaseController
import json
import logging
from os import path, walk
import ast
from formaters import WildCards

logger = logging.getLogger('la mirada de eduardo')


class Mappers(object):
    """
    Contenedor de los mappers.
    """

    def __init__(self, schema='default', version='1.0'):
        self.catalog = ''
        self.dataset = ''
        self.distribution = ''
        self.themeTaxonomy = ''
        if not self._load(schema, version):
            raise IOError('Imposble cargar mappers.')

    def _load(self, schema, version):
        """
        Carga las diferentes reglas de mapeos.

        Los mappers son archivos de tipo JSON que especifican que campo de
        CKAN se correspondra con que campo del catalogo.

        Se encuentran alojados en <plugin_folder>mappers/<mapper_name>/<mapper_version>/<filename>.json

        Todos los mapas, deben contar de al menos, cuatro archivos, correspondientes
        a cada parte del catalogo:

            - catalog
            - dataset
            - distribution
            - themeTaxonomy

        Args:
            - None.

        Returns:
             - Mappers: Clase contenedora de mapeos.
             - None: Fallo la carga de Mappers.
        """
        _errs = []
        wrk_folder = path.dirname(__file__)
        mappers_folder = path.join('mappers', '{schema}/{version}'.format(schema=schema,
                                                                          version=version))
        abs_path_mappers = path.join(wrk_folder, mappers_folder)

        # Chequeo que exista el schema seleccionado.
        if not path.exists(abs_path_mappers):
            err_msg = 'No es posible localizar el schema:{}, vesion:{}.'.format(schema, version)
            logger.critical(err_msg)
            raise IOError(err_msg)
        # Chequeo que existan todas la partes requeridas del schema.
        # dataset, distribution, catalog y themeTaxonomy

        for mapper in self.__dict__.keys():
            mfs = path.join(abs_path_mappers, '{}.json'.format(mapper))
            try:
                self.__dict__[mapper] = json.load(open(mfs))
            except IOError:
                err_msg = 'Fallo la carga del mapper: {}.'.format(mapper)
                logger.critical(err_msg)
                _errs.append(err_msg)
                return False
            except ValueError:
                err_msg = ('No es posible decodificar el mapper {},'
                           'no parece ser un JSON valido'.format(mapper))
                logger.critical(err_msg)
                _errs.append(err_msg)
                return False
        return True

    def __getitem__(self, item):
        if item not in self.__dict__.keys():
            err_msg = 'Mappers(class) no contiene el atributo {}'.format(item)
            logger.critical(err_msg)
            raise AttributeError(err_msg)
        return self.__dict__[item]

    def __iter__(self):
        for prop in self.__dict__.keys():
            yield self.__dict__[prop]

    def __setattr__(self, key, value):
        self.__dict__[key] = value


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
            return self.build_response(self.map_dataset(self.get_datasets()))
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

    def get_datasets(self):
        """
        Obtener lista de datasets contenidos dentro de CKAN.

        Returns:
            - List(). Len(list) == n: Lista de los n Dataset existentes en CKAN.
            - List(). Len(list) == 0: si ocurrio un error o no se han cargado datasets.
        """
        datasets = toolkit.get_action('package_search')(
            data_dict={
                'sort': 'metadata_modified desc',
                'rows': 5000})
        return datasets['results']

    def map_dataset(self, _datasets):
        maped_datasets = []
        for dataset in _datasets:
            mapped_dataset = {}
            for destination, origin in self.mappers.dataset['fields'].items():
                try:
                    if destination in self.mappers.dataset['patterns'].keys():
                        pattern = self.mappers.dataset['patterns'][destination]
                        pattern = self.wildcards.apply(_phrase=pattern)
                        if '@value' in pattern:
                            pattern = pattern.replace('@value', dataset[origin])
                        formated = pattern
                    else:
                        formated = dataset[origin]
                    mapped_dataset[destination] = formated

                except KeyError:
                    if '@datasets' in origin:
                        mapped_dataset[destination] = self.map_dataset(self.get_datasets())

                    if '@distributions' in origin:
                        mapped_dataset[destination] = self.map_themes(self.get_themes())

                    if '@themeTaxonomy' in origin:
                        mapped_dataset[destination] = self.map_themes(self.get_themes())

                    if destination not in self.mappers.dataset['required']:
                        pass
                    else:
                        raise KeyError
            if len(mapped_dataset.keys()) > 0:
                maped_datasets.append(mapped_dataset)
        return maped_datasets

    def get_themes(self):
        groups = toolkit.get_action('group_list')(
            data_dict={'all_fields': True})
        return groups

    def map_themes(self, _themes):
        mapped_themes = []
        for theme in _themes:
            mapped_theme = {}
            for destination, origin in self.mappers.themeTaxonomy['fields'].items():
                # TODO: implementar JSONSchema para esta clase de validaciones.
                if type(origin) in [unicode, str]:
                    try:
                        mapped_theme[destination] = theme[origin]
                    except KeyError:
                        if destination not in self.mappers.themeTaxonomy['required']:
                            pass
                        else:
                            raise KeyError
            mapped_themes.append(mapped_theme)
        return mapped_themes

    def build_response(self, _json_data):
        data = {}
        if type(_json_data) is dict or type(_json_data) is list:
            data = _json_data
        response.content_type = 'application/json; charset=UTF-8'
        del response.headers["Cache-Control"]
        del response.headers["Pragma"]
        return plugins.toolkit.literal(json.dumps(data))
