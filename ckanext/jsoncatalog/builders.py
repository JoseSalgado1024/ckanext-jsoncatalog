# -*- coding: utf-8 -*-
import ckan.plugins.toolkit as toolkit


class Catalog(object):
    def __init__(self):
        """
        Init de la clase Catalog()

        """

    @staticmethod
    def _get_ckan_data(_content_of='catalog',
                       dataset_id=-1):
        action_mapper = {
            'catalog': {
                'action': 'package_search',
                'datadict': {'sort': 'metadata_modified desc',
                             'rows': 5000}
            },
            'dataset': {
                'action': 'package_show',
                'datadict': {'sort': 'metadata_modified desc',
                             'id': dataset_id,
                             'rows': 5000}
            },
            'datasets': {
                'action': 'package_search',
                'datadict': {'sort': 'metadata_modified desc',
                             'rows': 5000},
                'sub_key': 'results'
            },
            'distributions': {
                'action': 'package_show',
                'datadict': {'sort': 'metadata_modified desc',
                             'id': dataset_id,
                             'rows': 5000}
            },
            'groups': {
                'action': 'group_list',
                'datadict': {'all_fields': True}
            },
        }
        if _content_of.lower() not in ['catalog',
                                       'dataset',
                                       'datasets',
                                       'distributions',
                                       'groups']:
            raise ValueError
        if not isinstance(dataset_id, int):
            raise TypeError
        if _content_of.lower() != 'dataset' and dataset_id > 0:
            raise TypeError
        sel_action = action_mapper[_content_of]
        _raw_data = toolkit.get_action(sel_action['action'])(data_dict=sel_action['datadict'])
        if sel_action['sub_key']:
            return _raw_data[sel_action['sub_key']]
        else:
            return _raw_data

    def _build_catalog(self):
        """

        :return:
        """
        _catalog_raw = self._get_ckan_data()
        _catalog = _catalog_raw
        return _catalog

    def __str__(self):
        """
        Renderizado del catalogo en JSON

        Returns:
            - Str().
        """
        import json
        catalog = {}
        try:
            catalog = self._build_catalog()
        except IOError:
            # Fallo en load.
            pass
        except ValueError:
            # Fallo en rq
            pass

        return json.dumps(catalog)
