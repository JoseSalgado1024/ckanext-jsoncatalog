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

    def _available_mappers(self):
        """
        Listado de mappers disponobles.

        Args:
            - None.

        Returns:
             - List(). listado de mappers disponibles.
        """
        return [mapper for mapper in self.__dict__.keys()]

    def apply(self, data=None,  _mapper='catalog'):
        def map_obj(_obj, mapper_selected):
            mapped_object = {}
            for destination, origin in mapper_selected['fields'].items():
                try:
                    if destination in mapper_selected['patterns'].keys():
                        pattern = mapper_selected['patterns'][destination]
                        pattern = wildcards.apply(_phrase=pattern)
                        if '@value' in pattern:
                            pattern = pattern.replace('@value', _obj[origin])
                        formated = pattern
                    else:
                        formated = _obj[origin]
                    mapped_object[destination] = formated

                except KeyError:
                    if '@' in origin:
                        mapped_object[destination] = origin
                    if destination not in selected_mapper['required']:
                        pass
                    else:
                        raise KeyError
            return mapped_object
        """
        Aplica un mapeo de datos preconfigurado.

        Args:
            - _mapper:

        Retunrs:
            - TODO!
        """
        if type(data) is None:
            raise TypeError('El campo \"data\" no admite el tipo: {}'.format(type(data)))
        if _mapper not in self._available_mappers():
            raise AttributeError('El mapper \"{}\" no existe.'.format(_mapper))
        wildcards = WildCards()
        selected_mapper = self.__dict__[_mapper]

        if type(data) is list:
            return [map_obj(obj, selected_mapper) for obj in data]
        elif type(data) is dict:
            return map_obj(data, selected_mapper)
        else:
            raise TypeError('Tipo de dato provisto no valido.')

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

    def get_ckan_data(self, _content_of='catalog'):
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
        maped_datasets = []
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
        return maped_datasets

    def get_themes(self):
        return self.get_ckan_data(_content_of='groups')

    def map_themes(self, _themes):
        mapped_themes = []
        try:
            mapped_themes = self.mappers.apply(_themes, _mapper='themeTaxonomy')
        except (AttributeError, TypeError, KeyError), e:
            print e
            # log entry
            pass
        return mapped_themes

    def build_response(self, _json_data):
        data = {}
        if type(_json_data) is dict or type(_json_data) is list:
            data = _json_data
        response.content_type = 'application/json; charset=UTF-8'
        del response.headers["Cache-Control"]
        del response.headers["Pragma"]
        return plugins.toolkit.literal(json.dumps(data))
