# -*- coding: utf-8 -*-
import logging


class CKANWrapper(object):
    def __init__(self, _wrapper_type='catalog', _mapper='default', _version='1.0'):
        from mappers import Mappers

        self.available_wrppers_type = ['dataset', 'themeTaxonomy', 'catalog', 'distribution']
        if _wrapper_type not in self.available_wrppers_type:
            raise TypeError
        self.mapper_name = _mapper
        self.mapper_version = _version
        self.wrapper_type = _wrapper_type
        self.mapper = Mappers(schema=_mapper, version=_version)
        self.logs = logging.getLogger('ckan.jsoncatalog.data_wrapper.{}'.format(self.wrapper_type))

    def translations(self, data=None, section='dataset'):
        """
        Traduccion de campos de ckan de CKAN.

        Args:
            - data:
            - section:

        Returns:
            - Dict.
        """

        def translate_list(_d, _listname):
            if _listname in _d:
                l = _d[_listname]
                new_obj = {}
                for o in l:
                    for k, v in o.items():
                        new_obj.update({'{}__{}'.format(_listname, k): v})
                if len(new_obj) > 0:
                    _d.update(new_obj)
            return _d

        def translate_extras(_d):
            if 'extras' in _d.keys():
                tmp_extras = _d['extras']
                tr_extras = {}
                for extra in tmp_extras:
                    tr_extras.update({'extras__{}'.format(extra['key']): extra['value']})
                if len(tr_extras) > 0:
                    _d.update(tr_extras)
            return _d

        if section.lower() not in self.available_wrppers_type:
            raise TypeError('No existe a seccion: {}.'.format(section))
        if section.lower() == 'dataset':
            return translate_list(translate_list(translate_extras(data), 'groups'), 'tags')

    def get_ckan_data(self):
        """
        Metodo unico para seleccionar las diferentes partes de la metadata de CKAN.

        Args:
            - _content_of: str. Area de matadata de ckan desde la cual se desea obtener informacion.
            - dataset_id: str. id de dataset.

        Returns:
            - TODO
        """

        action_mapper = {
            'catalog': {
                'action': 'package_search',
                'datadict': {'sort': 'metadata_modified desc',
                             'rows': 5000}
            },
            'dataset': {
                'action': 'package_search',
                'datadict': {'sort': 'metadata_modified desc',
                             'rows': 5000},
                'sub_key': 'results'
            },
            'themeTaxonomy': {
                'action': 'group_list',
                'datadict': {'all_fields': True}
            },
        }
        if self.wrapper_type.lower() not in ['catalog',
                                             'dataset',
                                             'datasets',
                                             'distributions',
                                             'themetaxonomy']:
            raise ValueError
        sel_action = action_mapper[self.wrapper_type]['action']
        _data_dict = action_mapper[self.wrapper_type]['datadict']
        self.logs.info('toolkit.get_action(\'{}\')({})'.format(sel_action, _data_dict))

        import ckan.plugins.toolkit as toolkit

        _raw_data = toolkit.get_action(sel_action)(data_dict=_data_dict)
        try:
            elem_list = _raw_data[action_mapper[self.wrapper_type]['sub_key']]
            for i in range(len(elem_list)):
                elem_list[i] = self.translations(data=elem_list[i], section=self.wrapper_type)
            return elem_list
        except KeyError:
            return _raw_data

    def _map(self, _data):
        return self.mapper.apply(_data, _mapper=self.wrapper_type)

    def post_map(self, _data):
        return _data

    def clean_temp_keys(self, _d):
        """

        :return:
        """
        if isinstance(_d, list):
            list_of_elem = []
            for e in _d:
                list_of_elem.append(self.clean_temp_keys(e))
            _d = list_of_elem
        if isinstance(_d, dict):
            for e in _d.keys():
                if '$$__TEMP__' in e:
                    del _d[e]
        return _d

    def build(self):
        """

        :return:
        """
        data = self.get_ckan_data()
        mapped_data = self._map(data)
        post_map_data = self.post_map(mapped_data)
        return self.clean_temp_keys(post_map_data)

    def render(self):
        """
        Renderizado del catalogo en JSON

        Returns:
            - Str().
        """
        r = {}
        try:
            self.logs.info('build...')
            r = self.build()
            self.logs.info('Hecho!')
        except IOError as e:
            self.logs.critical('Imposible realizar build. Imposible cargar {{mapper}}.json. Err:{}'.format(e))
        except ValueError as e:
            self.logs.critical('Imposible realizar build. {}'.format(e))
        return r if len(r) > 0 else None

    def __str__(self):
        import json
        return json.dumps(self.render())


class Catalog(CKANWrapper):
    def __init__(self, mapper='default', version='1.0'):
        """
        Init de la clase Catalog()

        """
        super(Catalog, self).__init__(_mapper=mapper, _version=version)

    def post_map(self, _data):
        for destination, origin in _data.items():
            if origin.lower() == '@datasets':
                _data.update({destination: Dataset(mapper=self.mapper_name,
                                                   version=self.mapper_version).render()})
            elif origin.lower() == '@themetaxonomy':
                _data.update({destination: ThemeTaxonomy(mapper=self.mapper_name,
                                                         version=self.mapper_version).render()})
        return _data


class Dataset(CKANWrapper):
    def __init__(self, mapper='default', version='1.0'):
        """
        Init de la clase Dataset()

        """
        super(Dataset, self).__init__(_wrapper_type='dataset',
                                      _mapper=mapper,
                                      _version=version)

    def post_map(self, _data):
        for i in range(len(_data)):
            for destination, origin in _data[i].items():
                if isinstance(origin, (str, unicode)):
                    if origin.lower() == '@distributions':
                        _data[i].update({destination: Distribution(mapper=self.mapper_name,
                                                                   version=self.mapper_version,
                                                                   distribution=_data[i][
                                                                       '$$__TEMP__distribution']).render()})
        return _data


class ThemeTaxonomy(CKANWrapper):
    def __init__(self, mapper='default', version='1.0'):
        """
        Init de la clase ThemeTaxonomy()

        """
        super(ThemeTaxonomy, self).__init__(_wrapper_type='themeTaxonomy',
                                            _mapper=mapper,
                                            _version=version)


class Distribution(CKANWrapper):
    def __init__(self, mapper='default', version='1.0', distribution=None):
        """
        Init de la clase Distribution().
        """
        self.distribution_raw = distribution
        super(Distribution, self).__init__(_wrapper_type='distribution',
                                           _mapper=mapper,
                                           _version=version)

    def get_ckan_data(self):
        return self.distribution_raw
