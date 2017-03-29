# coding: utf8
import logging
import json
from os import path
from formaters import *
from jsonschema.exceptions import *
import jsonschema

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
        if not self.load(schema, version):
            raise IOError('Imposble cargar mappers.')

    def validate_mapper(self, mapper_path):
        """
        Validacion de mappers.

        Returns:
            - Bool:
                - True: Es un mapper valido.
                - False: No es un mapper valido.
        """
        try:
            sv_path = path.join(path.dirname(__file__), 'validators/schema.validator.json')
            _valid_schema = json.load(open(sv_path))
            _mapper, _format = path.basename(mapper_path).split('.')
            if _mapper not in self.__dict__.keys():
                raise KeyError
            if _format.lower() not in ['json']:
                raise TypeError
            if not path.exists(mapper_path):
                raise IOError
            _loaded_mapper = json.load(open(mapper_path))
            jsonschema.validate(_loaded_mapper, _valid_schema)
            return True
        except (IOError, KeyError):
            return False
        except ValidationError:
            return False

    def load(self, schema, version):
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
        result = False
        wrk_folder = path.dirname(__file__)
        mappers_folder = path.join('mappers', '{schema}/{version}'.format(schema=schema,
                                                                          version=version))
        abs_path_mappers = path.join(wrk_folder, mappers_folder)

        # Chequeo que exista el schema seleccionado.
        if not path.exists(abs_path_mappers):
            raise IOError

        # Chequeo que existan todas la partes requeridas del schema.
        # dataset, distribution, catalog y themeTaxonomy
        load_results = []
        for mapper in self.__dict__.keys():
            mfs = path.join(abs_path_mappers, '{}.json'.format(mapper))
            try:
                result = self.validate_mapper(mfs)
                if result:
                    self.__dict__[mapper] = json.load(open(mfs))
                    if mapper == 'dataset':
                        self.__dict__[mapper]['fields'].update({'$$__TEMP___distribution': 'resources'})
            except IOError:
                logger.critical('Fallo la carga del mapper: {}.'.format(mapper))
            except ValueError:
                logger.critical('No es posible decodificar el mapper {}, no es JSON valido'.format(mapper))
            load_results.append(result)
        return False not in load_results

    def available_mappers(self):
        """
        Listado de mappers disponobles.

        Args:
            - None.

        Returns:
             - List(). listado de mappers disponibles.
        """
        return [mapper for mapper in self.__dict__.keys()]

    def apply(self, data=None, _mapper='catalog'):
        """
        Aplica un mapeo de datos pre-configurado.

        Args:
            - _mapper:

        Returns:
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
                        pass
            return mapped_object

        if data in [None]:
            raise TypeError('El campo \"data\" no admite el tipo: {}'.format(type(data)))
        if _mapper not in self.available_mappers():
            raise AttributeError('El mapper \"{}\" no existe.'.format(_mapper))
        wildcards = WildCards()
        selected_mapper = self.__dict__[_mapper]

        if isinstance(data, list):
            list_of_items = []
            for o in data:
                list_of_items.append(self.apply(data=o, _mapper=_mapper))
                #  list_of_item.append(map_obj(o, selected_mapper))
            return list_of_items
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
