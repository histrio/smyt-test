"""
File: __init__.py
Author: Rinat F Sabitov
Description: hail pep302
"""

import imp
import os.path
import sys
import yaml
import json

from functools import partial
from django.http import HttpResponse

VERSION = (0, 0, 1, 'rc', 1)


def get_version(version=None):
    "Returns a PEP 386-compliant version number from VERSION."
    if version is None:
        version = VERSION


class SmytException(Exception):
    pass


def get_field(id, title, type):
    """ Return appropriate field or raise error
    """
    from django.db.models import CharField, IntegerField, DateField
    mapping = {
        'char': partial(CharField, max_length=20),
        'int': IntegerField,
        'date': DateField,
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
    """ Unified view for get / create / update requests
    """
    class PostRequestException(Exception):
        pass

    def get(self, request, *args, **kwargs):
        from django.core import serializers
        from django.http import HttpResponse
        queryset = self.model.objects.all()
        data = serializers.serialize('json', queryset)
        return HttpResponse(data, content_type='application/json')

    def bind_from(self, data):
        if 'id' in data:
            try:
                obj = self.model.objects.get(id=data.get('id'))
            except self.model.DoesNotExist:
                obj = self.model()
            obj.__dict__.update(**data.dict())
        else:
            obj = self.model.objects.create(**data)
        return obj

    def post(self, request, *args, **kwargs):
        result = {'success': True, 'message': 'Record saved'}
        try:
            obj = self.bind_from(request.POST.copy())
            obj.save()
        except self.PostRequestException as err:
            result = {'success': False, 'message': "Saving error: %s" % err}

        return HttpResponse(json.dumps(result), content_type='application/json')


class YamlModelsLoader(object):
    """ Module finder/loader.
    Looking for imports which ends with `yaml` and
    try to parse it for the great good
    """

    yaml_filename = None
    fullname = None
    models_dict = None

    def find_module(self, fullname, paths=None):
        for path in (paths or sys.path + [os.path.dirname(__file__), ]):
            filename = os.path.abspath(os.path.join(
                path, "%s.yaml" % fullname.rsplit('.')[-1]))
            if os.path.isfile(filename):
                self.fullname = fullname
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
        if not data:
            return result
        for table, params in data.items():
            model_name = '%sModel' % table.capitalize()
            try:
                attrs = get_attr(**params)
            except TypeError as err:
                raise SmytException('Invalid yaml file format.')
            attrs.update({
                '__module__': self.fullname + '.yaml.models'
            })
            from django.db.models import Model
            model = type(model_name, (Model, ), attrs)
            result[model_name] = model
        return result

    def get_admin(self, models_dict):
        from django.contrib.admin import ModelAdmin, site
        from django.contrib.admin.sites import AlreadyRegistered
        result = {}
        for model_name, model in models_dict.items():
            model_admin = type(model_name + 'Admin', (ModelAdmin, ), {
                '__module__': self.fullname + '.yaml.admin',
            })
            result[model_name + 'Admin'] = model_admin
            try:
                site.register(model, model_admin)
            except AlreadyRegistered:
                pass
        return result

    def get_views(self, models_dict):
        result = {}
        for model_name, model in models_dict.items():
            from django.views.generic.base import View
            list_view = type(model_name + 'ListView',
                (SmytResponseMixin, View), {
                    'model': model
                }
            )
            result[model_name + 'ListView'] = list_view
            result[model._meta.db_table + '_list_view'] = list_view.as_view()
        return result

    def get_urls(self, models_dict):
        from django.conf.urls import url

        patterns = [
            url(r'^%s/$' % model._meta.db_table, '%s.views.%s' % (
                model.__module__.rsplit('.', 1)[0],
                model._meta.db_table + '_list_view'
            )) for model_name, model in models_dict.items()
        ]

        result = {
            'urlpatterns': patterns
        }
        return result

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
