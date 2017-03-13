# coding: utf8

from os import environ
import ckan.model as model
from ckan.config.environment import config
import arrow
import dateutil


class WildCards(object):
    """
    TODO: Documentar clase.
    """
    def __init__(self):

        self.site_url = config.get('ckan.site_url')

    @property
    def actual_date(self):
        """
        Date Actual.
        Returns:
            - Date-ISO8601. Str()
        """
        return arrow.now().format('YYYY-MM-DD_HH:ss:mm')

    @property
    def dataset_counter(self):
        """
        Cantidad de Datasets en la plataforma.

        Returns:
            - Int().

        """
        return 0

    def list(self):
        return [wildcard for wildcard in self.__dict__.keys()]

    def apply(self, _phrase):
        """
        Aplica las WildCards a una phrase provista en _phrase.

        Args:
            - _phrase: Str().
        Retunrs:
            - _phrase: Str().
        """
        for name in self.__dict__.keys():
            if name in _phrase:
                wc_name = '@{}'.format(name)
                _phrase = _phrase.replace(wc_name, self.__dict__[name])
        return _phrase

    def __iter__(self):
        """
        Itera sobre las propiedades de la clase.

        Args:
            - None.

        Returns:
            - TODO:
        """
        for prop in self.__dict__.keys():
            yield self.__dict__[prop]

    def __getitem__(self, item):
        """
        Seleccion de propiedades de la clase en formato dict().

        Args:
            - item:
        Return:
            - Existe: Contenido de la propiedad.
            - No Existe: Raise AttributeError.
        """
        if item not in self.__dict__.keys():
            raise AttributeError('No existe metodo {}.'.format(item))
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
