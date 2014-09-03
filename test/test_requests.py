import sys
import os
from django.test import TestCase
from django.test import Client

sys.path.insert(0, os.path.abspath('./src'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'task.settings'
from django.core.management import call_command
import json


class RequetsTest(TestCase):

    def setUp(self):
        self.client = Client()
        call_command('syncdb', all=True, interactive=False, noinput=True, )

    def tearDown(self):
        call_command('flush', interactive=False, noinput=True)

    def test_meta_request(self):

        response = self.client.get("/")
        assert response.status_code == 200

        import json
        response = self.client.get("/smyt_items/")
        data = json.loads(response.content)

        for item in data:
            assert 'url' in item and 'fields' in item and 'title' in item

    def test_get_request(self):
        response = self.client.get("/smyt_items/yaml_roomsmodel/")
        assert len(json.loads(response.content)) == 0

        from smytmodels.yaml import models
        models.RoomsModel.objects.create(
            spots=5,
            department='test'
        )
        response = self.client.get("/smyt_items/yaml_roomsmodel/")
        assert len(json.loads(response.content)) == 1

    def test_post_request(self):
        response = self.client.post("/smyt_items/yaml_roomsmodel/",
                data={'id': 1, 'spots': '2', 'department': 'test'})
        assert json.loads(response.content)['success'] is True

        response = self.client.post("/smyt_items/yaml_roomsmodel/",
                data={'spots': '2', 'department': 'test'})
        assert json.loads(response.content)['success'] is True

        from smytmodels.yaml import models
        assert models.RoomsModel.objects.all().count() == 2
