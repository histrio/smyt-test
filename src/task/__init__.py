"""
File: __init__.py
Author: Rinat F Sabitov
Description: hail pep302
"""

import imp
import os.path
import sys
import yaml

from django.db import models
from django.contrib.admin import ModelAdmin, site
from functools import partial

class SmytException(Exception):
    pass


def get_field(id, title, type):
    mapping = {
        'char': partial(models.CharField, max_length=20, verbose_name=title),
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
    result = {
        #'__module__': 'task.smyt.models',
    }
    for field in fields:
        try:
            result[field['id']] = get_field(**field)
        except KeyError:
            raise SmytException("Field's `id` not found")

    meta = type('Meta', (), {
        'verbose_name': title,
    })
    result['Meta'] = meta
    return result



class YamlModelsLoader(object):
    """ Module finder/loader.
    Looking for imports which ends with `yaml` and
    try to parse it for the great good
    """

    yaml_filename = None
    fullname = None

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
        from django.views.generic import ListView
        for model_name, model in models_dict.items():
            list_view = type(model_name+'ListView', (ListView, ), {
                'model': model
            })
            result[model_name+'ListView'] = list_view
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

        #def extend_module(module, module_name, attrs):
            #mod_name = '.'.join(yaml_fullname, module_name)
            #mod = imp.new_module(mod_name)
            #sys.modules[mod_name] = mod
            #mod.__file__ = self.yaml_filename
            #mod.__dict__.update(attrs if not callable(attrs) else attrs())
            #setattr(yaml_mod, module_name, mod)

        ##models = self.get_models()
        #extend_module('models', self.get_models)
        #extend_module('admin', self.get_admin(models))
        #extend_module('migrations', {})
        #extend_module('views', self.get_views(models))



        models_mod = imp.new_module(yaml_fullname+'.models')
        models_mod.__file__ = self.yaml_filename
        sys.modules[yaml_fullname+'.models'] = models_mod
        models_dict = self.get_models()
        models_mod.__dict__.update(models_dict)

        admin_mod = imp.new_module(yaml_fullname+'.admin')
        admin_mod.__file__ = self.yaml_filename
        admin_dict = self.get_admin(models_dict)
        admin_mod.__dict__.update(admin_dict)
        sys.modules[yaml_fullname+'.admin'] = admin_mod


        views_mod = imp.new_module(yaml_fullname+'.views')
        views_mod.__file__ = self.yaml_filename
        views_dict = self.get_views(models_dict)
        views_mod.__dict__.update(views_dict)
        sys.modules[yaml_fullname+'.views'] = views_mod

        migrations_mod = imp.new_module(yaml_fullname+'.migrations')
        migrations_mod.__file__ = os.path.join(
            os.path.dirname(self.yaml_filename),
            'migrations.__init__.py')
        sys.modules[yaml_fullname+'.migrations'] = migrations_mod

        yaml_mod.models = models_mod
        yaml_mod.admin = admin_mod
        yaml_mod.migrations = migrations_mod
        yaml_mod.views = views_mod
        return mod


sys.meta_path.append(YamlModelsLoader())
