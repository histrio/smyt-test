import sys
import os
import django.conf
from django.test import TestCase
#from unittest import TestCase
from django.test import Client

sys.path.insert(0, os.path.abspath('./src'))
os.environ['DJANGO_SETTINGS_MODULE']='task.settings'
from django.test.utils import override_settings
from django.test.utils import setup_test_environment

from django.core.management import call_command

from django.test import simple
import json

class RequetsTest(TestCase):

    def setUp(self):
        setup_test_environment()
        runner = simple.DjangoTestSuiteRunner(verbosity=0)
        self.client = Client()
        #runner.setup_databases()

    def test_meta_request(self):

        response = self.client.get("/")
        assert response.status_code == 200

        import json
        response = self.client.get("/smyt_items/")
        data = json.loads(response.content)

        for item in data:
            assert 'url' in item and 'fields' in item and 'title' in item

    #from django.conf import settings
    #@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS+('smytmodels.yaml', ))
    def test_get_request(self):
        call_command('syncdb', interactive=False, noinput=True)
        call_command('migrate', noinput=True)
        response = self.client.get("/smyt_items/yaml_roomsmodel/")
        assert len(json.loads(response.content)) == 0

        from smytmodels.yaml import models
        models.RoomsModel.objects.create(
            spots=5,
            department='test'
        )
        response = self.client.get("/smyt_items/yaml_roomsmodel/")
        assert len(json.loads(response.content)) == 1

    #@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS+('smytmodels.yaml', ))
    def test_post_request(self):
        #call_command('syncdb', interactive=False, noinput=True)
        #call_command('migrate', noinput=True)
        response = self.client.post("/smyt_items/yaml_roomsmodel/",
            data={'id':1})
        print response.content
        assert json.loads(response.content)['success'] == True
