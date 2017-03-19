# encoding: utf-8

"""
Tests for the ckanext.jsoncatalog extension.

"""
from nose.tools import assert_raises
from nose.tools import assert_equal
import ckan.model as model
import ckan.plugins
import ckan.tests.factories as factories
import ckan.logic as logic


class TestPluginParentJsoncatalog(object):
    """

    """
    @classmethod
    def setup_class(cls):
        """Nose runs this method once to setup our test class."""
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        ckan.plugins.load('jsoncatalog')

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
        ckan.plugins.unload('jsoncatalog')

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