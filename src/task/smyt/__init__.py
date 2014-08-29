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
        raise SmytException('Unkown field type: expected int/char/date, got `%s`' % type )
    return field


def get_attr(title, fields):
    """ Returns dict with appropriate django model fields.
    """
    result = {
        '__module__': 'task.smyt.models',
    }
    for field in fields:
        #result['name'] =
        result[field['id']] = get_field(**field)

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

    def find_module(self, fullname, paths=None):
        if paths is not None:
            for path in paths:
                self.yaml_filename = os.path.join(
                    path, "%s.yaml" % fullname.rsplit('.')[-1])
                if os.path.isfile(self.yaml_filename):
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
            model = type(model_name, (models.Model, ), attrs)
            result[model_name] = model

        import admin
        #sorry, but monkeypatching
        for model in result.values():
            model_admin = type(model_name + 'Admin', (ModelAdmin, ), {
                '__module__': 'task.smyt.admin',
            })
            setattr(admin, model_name + 'Admin', model_admin)
            site.register(model, model_admin)
        return result

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        yaml_fullname = fullname + '.yaml'
        mod = imp.new_module(fullname)
        mod.__loader__ = self
        mod.__file__ = self.yaml_filename
        mod.__path__ = []
        sys.modules[fullname] = mod
        yaml_mod = imp.new_module(yaml_fullname)

        yaml_mod.__dict__.update(self.get_models())
        sys.modules[yaml_fullname] = yaml_mod
        return mod

# activate import hook
sys.meta_path.append(YamlModelsLoader())
