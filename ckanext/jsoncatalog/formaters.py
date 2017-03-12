from os import environ
import ckan.model as model
from ckan.config.environment import config


class WildCards(object):
    def __init__(self):
        self.site_url = config.get('ckan.site_url')

    def apply(self, _phrase):
        """

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

    def items(self):
        return self.__dict__.items()

    def keys(self):
        return self.__dict__.keys()

    def __iter__(self):
        for prop in self.__dict__.keys():
            yield self.__dict__[prop]

    def __getitem__(self, item):
        if item not in self.__dict__.keys():
            raise AttributeError(err_msg)
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
