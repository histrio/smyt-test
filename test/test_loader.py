
import sys
import os
import django.conf
from unittest import TestCase

from task import SmytException
from nose.tools import raises

sys.path.insert(0, os.path.abspath('./src'))
os.environ['DJANGO_SETTINGS_MODULE']='task.settings'

class YamlLoaderTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
                INSTALLED_APPS=[
                    'test.app.yaml',
                ]
            )

    def test_models(self):
        from test.app.yaml import models
        from django.db.models import fields
        assert hasattr(models, 'FirsttesttableModel')

        int_field = models.FirsttesttableModel._meta.get_field_by_name('code')[0]
        assert isinstance(int_field, fields.IntegerField)

        char_field = models.FirsttesttableModel._meta.get_field_by_name('name')[0]
        assert isinstance(char_field, fields.CharField)

        date_field = models.FirsttesttableModel._meta.get_field_by_name('date')[0]
        assert isinstance(date_field, fields.DateField)

        assert hasattr(models, 'SecondtesttableModel')

        assert models.SecondtesttableModel._meta.verbose_name=='Another test title'
        field = models.SecondtesttableModel._meta.get_field_by_name('some_value')[0]
        assert field.verbose_name=='some value'


    def test_admin(self):
        from test.app.yaml import admin
        assert hasattr(admin, 'FirsttesttableModelAdmin')
        assert hasattr(admin, 'SecondtesttableModelAdmin')

    def test_views(self):
        from test.app.yaml import views

    def test_urls(self):
        from test.app.yaml import urls

class EmptyYamlLoaderTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
                INSTALLED_APPS=[
                    'test.empty.yaml',
                ]
            )

    def test_models(self):
        from test.app.yaml import models

class InvalidOneYamlLoaderTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
                INSTALLED_APPS=[
                    'test.invalid01.yaml',
                ]
            )

    @raises(SmytException)
    def test_models(self):
        from test.invalid01.yaml import models

class InvalidTwoYamlLoaderTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
                INSTALLED_APPS=[
                    'test.invalid02.yaml',
                ]
            )

    @raises(SmytException)
    def test_models(self):
        from test.invalid02.yaml import models


class InvalidThreeYamlLoaderTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
                INSTALLED_APPS=[
                    'test.invalid03.yaml',
                ]
            )

    @raises(SmytException)
    def test_models(self):
        from test.invalid03.yaml import models

class InvalidFourYamlLoaderTest(TestCase):

    def setUp(self):
        if not django.conf.settings.configured:
            django.conf.settings.configure(
                default_settings=django.conf.global_settings,
                INSTALLED_APPS=[
                    'test.invalid04.yaml',
                ]
            )

    @raises(SmytException)
    def test_models(self):
        from test.invalid04.yaml import models
