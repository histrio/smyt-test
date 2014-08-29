import imp
import os.path
import sys


class YamlModelsLoader(object):
    def find_module(self, fullname, paths=None):
        if paths is not None:
            for path in paths:
                filename = os.path.join(path, "%s.yaml" % fullname.rsplit('.')[-1])
                if os.path.isfile(filename):
                    return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        mod = imp.new_module(fullname)
        mod.__loader__ = self
        mod.__file__ = ''
        mod.__path__ = []
        sys.modules[fullname] = mod
        mod.yaml = imp.new_module(fullname+'.yaml')
        sys.modules[fullname+'.yaml'] = mod.yaml
        print mod
        return mod

sys.meta_path.append(YamlModelsLoader())
