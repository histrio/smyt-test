
import sys
import os
import django.conf
from django.test import TestCase
#from unittest import TestCase
from django.test import Client

sys.path.insert(0, os.path.abspath('./src'))
os.environ['DJANGO_SETTINGS_MODULE']='task.settings'
from django.test.utils import override_settings

class RequetsTest(TestCase):

    def setUp(self):
        self.client = Client()
        #if not django.conf.settings.configured:
            #django.conf.settings.configure(
                #default_settings=django.conf.global_settings,
                #INSTALLED_APPS=[
                    #'test.app.yaml',
                #]
            #)

    @override_settings(INSTALLED_APPS=['test.app.yaml', ])
    def test_meta_request(self):

        response = self.client.get("/")
        assert response.status_code == 200

        import json
        response = self.client.get("/smyt_items/")
        data = json.loads(response.content)

        for item in data:
            assert 'url' in item and 'fields' in item and 'title' in item

    #@override_settings(PROJECT_APPS=['test.app.yaml', ])
    #def test_get_request(self):
        #response = self.client.get("/smyt_items/yaml_firsttesttablemodel/")

