# coding: utf8
import logging
import json
from os import path
from formaters import *
logger = logging.getLogger(__name__)


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
              raise IOError

        # Chequeo que existan todas la partes requeridas del schema.
        # dataset, distribution, catalog y themeTaxonomy
        for mapper in self.__dict__.keys():
            mfs = path.join(abs_path_mappers, '{}.json'.format(mapper))
            try:
                self.__dict__[mapper] = json.load(open(mfs))
            except IOError:
                err_msg = 'Fallo la carga del mapper: {}.'.format(mapper)
            except ValueError:
                err_msg = ('No es posible decodificar el mapper {}, no es JSON valido'.format(mapper))
            finally:
                _errs.append(err_msg)
                logger.critical(err_msg)
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
        """
        Aplica un mapeo de datos preconfigurado.

        Args:
            - _mapper:

        Retunrs:
            - TODO!
        """

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

        if data in [None]:
            raise TypeError('El campo \"data\" no admite el tipo: {}'.format(type(data)))
        if _mapper not in self._available_mappers():
            raise AttributeError('El mapper \"{}\" no existe.'.format(_mapper))
        wildcards = WildCards()
        selected_mapper = self.__dict__[_mapper]

        if isinstance(data, list):
            return [map_obj(obj, selected_mapper) for obj in data]
        elif isinstance(data, dict):
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

