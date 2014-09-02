"""
File: __init__.py
Author: Rinat F Sabitov
Description: hail pep302
"""

import imp
import os.path
import sys
from functools import partial

import yaml
from django.db import models
from django.contrib.admin import ModelAdmin, site
from django.core import serializers
from django.http import HttpResponse
from django.conf.urls import url
from django.views.generic.list import BaseListView


class SmytException(Exception):
    pass


def get_field(id, title, type):
    """ Return appropriate field or raise error
    """
    mapping = {
        'char': partial(models.CharField, max_length=20),
        'int': models.IntegerField,
        'date': models.DateField,
    }
    try:
        field = mapping[type](verbose_name=title)
    except KeyError:
        raise SmytException('Unkown field type: expected '
            'int/char/date, got `%s`' % type)
    return field


def get_attr(title, fields):
    """ Returns dict with appropriate django model fields.
    """
    result = {}
    for field in fields:
        try:
            result[field['id']] = get_field(**field)
        except KeyError:
            raise SmytException("Field's `id` not found")
    result['is_smyt'] = True
    meta = type('Meta', (), {
        'verbose_name': title,
    })
    result['Meta'] = meta
    return result



class SmytResponseMixin(object):
    """ Return json
    """
    def render_to_response(self, context):
        if self.request.method == 'GET':
            queryset = self.model.objects.all()
            data = serializers.serialize('json', queryset)
            return HttpResponse(data, content_type='application/json')
        elif self.request.method == 'POST':
            return HttpResponse("{}", content_type='application/json')


class YamlModelsLoader(object):
    """ Module finder/loader.
    Looking for imports which ends with `yaml` and
    try to parse it for the great good
    """

    yaml_filename = None
    fullname = None
    models_dict = None

    def find_module(self, fullname, paths=None):
        for path in (paths or ['./task/', ]):
            self.fullname = fullname
            filename = os.path.join(
                path, "%s.yaml" % fullname.rsplit('.')[-1])
            if os.path.isfile(filename):
                self.yaml_filename = filename
                return self
        return None

    def get_models(self):
        result = {}
        with open(self.yaml_filename, 'r') as f:
            try:
                data = yaml.load(f)
            except yaml.YAMLError as err:
                raise SmytException('YAML file parsing error: %s' % err)

        for table, params in data.items():
            model_name = '%sModel' % table.capitalize()
            try:
                attrs = get_attr(**params)
            except TypeError as err:
                raise SmytException('Invalid yaml file format.')
            attrs.update({
                '__module__':self.fullname+'.yaml.models'
            })
            model = type(model_name, (models.Model, ), attrs)
            result[model_name] = model
        return result

    def get_admin(self, models_dict):
        result = {}
        for model_name, model in models_dict.items():
            model_admin = type(model_name + 'Admin', (ModelAdmin, ), {
                '__module__': self.fullname+'.yaml.admin',
            })
            result[model_name + 'Admin'] = model_admin
            site.register(model, model_admin)
        return result

    def get_views(self, models_dict):
        result = {}
        for model_name, model in models_dict.items():
            list_view = type(model_name+'ListView', (SmytResponseMixin, BaseListView, ), {
                'model': model
            })
            result[model_name+'ListView'] = list_view
            result[model._meta.db_table+'_list_view'] = list_view.as_view()
        return result

    def get_urls(self, models_dict):
        return {
            'urlpatterns': [
                url(r'^%s/$' % model._meta.db_table, '%s.views.%s' % (
                    model.__module__.rsplit('.', 1)[0],
                    model._meta.db_table+'_list_view'
                )) for model_name, model in models_dict.items()
            ]
        }


    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        yaml_fullname = fullname + '.yaml'
        mod = imp.new_module(fullname)
        mod.__loader__ = self
        mod.__file__ = self.yaml_filename
        sys.modules[fullname] = mod

        yaml_mod = imp.new_module(yaml_fullname)
        yaml_mod.__file__ = self.yaml_filename
        mod.yaml = yaml_mod
        sys.modules[yaml_fullname] = yaml_mod

        def extend_module(module_name):
            mod_name = '.'.join([yaml_fullname, module_name, ])
            mod = imp.new_module(mod_name)
            sys.modules[mod_name] = mod
            mod.__file__ = self.yaml_filename
            return mod

        yaml_mod.models = extend_module('models')
        models_dict = self.get_models()
        yaml_mod.models.__dict__.update(models_dict)

        yaml_mod.admin = extend_module('admin')
        yaml_mod.admin.__dict__.update(self.get_admin(models_dict))

        try:
            import task.migrations
            yaml_mod.migrations = task.migrations
        except ImportError:
            pass

        yaml_mod.views = extend_module('views')
        yaml_mod.views.__dict__.update(self.get_views(models_dict))

        yaml_mod.urls = extend_module('urls')
        yaml_mod.urls.__dict__.update(self.get_urls(models_dict))
        return mod

sys.meta_path.append(YamlModelsLoader())
