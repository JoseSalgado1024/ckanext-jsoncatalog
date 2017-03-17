# encoding: utf-8

"""
Tests for the ckanext.jsoncatalog extension.

"""
import paste.fixture
import pylons.test
import webtest

from nose.tools import assert_raises
from nose.tools import assert_equal

import ckan.model as model
import ckan.tests.legacy as tests
import ckan.plugins
import ckan.tests.factories as factories
import ckan.logic as logic
from ckan.common import config

class TestJsocatalogFunctionsPluginV6ParentJsoncatalog(object):
    """Tests for the ckanext.example_iauthfunctions.plugin module.

    Specifically tests that overriding parent auth functions will cause
    child auth functions to use the overridden version.
    """
    @classmethod
    def setup_class(cls):
        """Nose runs this method once to setup our test class."""
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        ckan.plugins.load('jsoncatalog_v6_parent_jsoncatalog')

    def teardown(self):
        """Nose runs this method after each test method in our test class."""
        # Rebuild CKAN's database after each test method, so that each test
        # method runs with a clean slate.
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        """
        Nose runs this method once after all the test methods in our class
        have been run.

        """
        # We have to unload the plugin we loaded, so it doesn't affect any
        # tests that run after ours.
        ckan.plugins.unload('jsoncatalog_v6_parent_jsoncatalog')

    def test_resource_delete_editor(self):
        """Normally organization admins can delete resources
        Our plugin prevents this by blocking delete organization.

        Ensure the delete button is not displayed (as only resource delete
        is checked for showing this)

        """
        user = factories.User()
        owner_org = factories.Organization(
            users=[{'name': user['id'], 'capacity': 'admin'}]
        )
        dataset = factories.Dataset(owner_org=owner_org['id'])
        resource = factories.Resource(package_id=dataset['id'])
        with assert_raises(logic.NotAuthorized) as e:
            logic.check_access('resource_delete', {'user': user['name']},
                               {'id': resource['id']})

        assert_equal(e.exception.message, 'User %s not authorized to delete resource %s' % (user['name'],
                                                                                            resource['id']))

    def test_resource_delete_sysadmin(self):
        """Normally organization admins can delete resources
        Our plugin prevents this by blocking delete organization.

        Ensure the delete button is not displayed (as only resource delete
        is checked for showing this)

        """
        user = factories.Sysadmin()
        owner_org = factories.Organization(
            users=[{'name': user['id'], 'capacity': 'admin'}]
        )
        dataset = factories.Dataset(owner_org=owner_org['id'])
        resource = factories.Resource(package_id=dataset['id'])
        assert_equal(logic.check_access('resource_delete', {'user': user['name']}, {'id': resource['id']}), True)


class TestJsoncatalogCustomConfigSetting(object):
    '''Tests for the plugin_v5_custom_config_setting module.

    '''
    def _get_app(self, users_can_create_groups):

        # Set the custom config option in config.
        config['ckan.jsoncatalog.users_can_create_groups'] = (
            users_can_create_groups)

        # Return a test app with the custom config.
        app = ckan.config.middleware.make_app(config['global_conf'], **config)
        app = webtest.TestApp(app)

        ckan.plugins.load('jsoncatalog_v5_custom_config_setting')

        return app

    def teardown(self):

        # Remove the custom config option from config.
        del config['ckan.jsoncatalog.users_can_create_groups']

        # Delete any stuff that's been created in the db, so it doesn't
        # interfere with the next test.
        model.repo.rebuild_db()

    @classmethod
    def teardown_class(cls):
        ckan.plugins.unload('jsoncatalog_v5_custom_config_setting')

    def test_sysadmin_can_create_group_when_config_is_False(self):
        app = self._get_app(users_can_create_groups=False)
        sysadmin = factories.Sysadmin()

        tests.call_action_api(app, 'group_create', name='test-group',
                              apikey=sysadmin['apikey'])

    def test_user_cannot_create_group_when_config_is_False(self):
        app = self._get_app(users_can_create_groups=False)
        user = factories.User()

        tests.call_action_api(app, 'group_create', name='test-group',
                              apikey=user['apikey'], status=403)

    def test_visitor_cannot_create_group_when_config_is_False(self):
        app = self._get_app(users_can_create_groups=False)

        tests.call_action_api(app, 'group_create', name='test-group',
                              status=403)

    def test_sysadmin_can_create_group_when_config_is_True(self):
        app = self._get_app(users_can_create_groups=True)
        sysadmin = factories.Sysadmin()

        tests.call_action_api(app, 'group_create', name='test-group',
                              apikey=sysadmin['apikey'])

    def test_user_can_create_group_when_config_is_True(self):
        app = self._get_app(users_can_create_groups=True)
        user = factories.User()

        tests.call_action_api(app, 'group_create', name='test-group',
                              apikey=user['apikey'])

    def test_visitor_cannot_create_group_when_config_is_True(self):
        app = self._get_app(users_can_create_groups=True)

        tests.call_action_api(app, 'group_create', name='test-group',
                              status=403)

