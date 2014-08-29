"""
File: __init__.py
Author: Rinat F Sabitov
Description:
"""

import imp
import os.path
import sys
import yaml

from django.db import models
from django.contrib.admin import ModelAdmin, site


def get_attr(title, fields):
    result = {
        '__module__': 'task.smyt.models',
    }
    result['name'] = models.CharField(max_length=20)

    meta = type('Meta', (), {
        'verbose_name': title,
    })
    result['Meta'] = meta
    return result


class YamlModelsLoader(object):

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
            data = yaml.load(f)
        for table, params in data.items():
            model_name = '%sModel' % table.capitalize()
            attrs = get_attr(**params)
            model = type(model_name, (models.Model, ), attrs)
            result[model_name] = model

        import admin
        for model in result.values():
            model_admin = type(model_name + 'Admin', (ModelAdmin, ), {
                '__module__': 'task.smyt.admin',
            })
            setattr(admin, model_name + 'Admin', model_admin)
            site.register(model, model_admin)
            print dir(admin)
        return result

    def get_admin(self):
        pass

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

sys.meta_path.append(YamlModelsLoader())
