from django.test.runner import DiscoverRunner

# A test runner that doesn't trigger any db backup
# Can be used setting TEST_RUNNER='js_reverse.tests.NoDbTestRunner.NoDbTestRunner'
# in the project settings.py
#
#               !!!! IMPORTANT !!!!
#
# Used ONLY to test the app in a dedicated test project
#          DO NOT USE THIS IN PRODUCTION!
#
#               !!!! IMPORTANT !!!!

# adapted from http://stackoverflow.com/a/7004517/4046810
class NoDbTestRunner(DiscoverRunner):
  """ A test runner to test without database creation """

  def setup_databases(self, **kwargs):
    """ Override the database creation defined in parent class """
    pass

  def teardown_databases(self, old_config, **kwargs):
    """ Override the database teardown defined in parent class """
    pass