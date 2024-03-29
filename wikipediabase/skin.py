"""
To configure a skin we have skin configurator objects. Skin
configurators are dict-like objects that provide data to the
skin. Then skins are organized in layers each layer overriding all the
previous. To define your project create a skin and it's configurator
so that people can use your package independently.
"""

from functools import reduce

import json

class DictSkinConfig(dict):
    def __init__(self, *args, **kwargs):
        super(DictSkinConfig, self).__init__(*args, **kwargs)

    def dump(self, dic):
        """
        Dump as json.
        """

        return json.dumps(dic)

class JsonSkinConfig(object):
    def __init__(self, data=None, filename=None, string=None):
        """
        Set from where to read data. data isn't actually read until get is
        called for the first time. String overrides the filename.
        """

        self.filename = filename
        self.string = string
        self.data = data

    def get(self, attr):
        """
        Lazily get attributes from json string or file.
        """

        try:
            return self.data.get(attr)
        except AttributeError:
            if self.filename is self.string is None:
                return None

            if self.string is None:
                with open(self.filename) as fd:
                    self.string = fd.read()

            self.data = json.loads(self.string)
            return self.data.get(attr)

    def keys(self):
        """
        Get all available keys.
        """

        try:
            return self.data.keys()
        except AttributeError:
            return []

    def dump(self, dic):
        """
        Dump a string from dict.
        """

        return json.dumps(dic)


class Skin(object):
    """
    A hierarchy of layers of skins. There are 3 sources of attributes
    for this.

    - Previous skins
    - Current config
    - Programmatically set configs.
    """

    def __init__(self, config=None, local=None, parent=None, dumper=None):
        """
        Config needs only implement get and keys. Create a configuration
        skin. dumper need to implement dump(). No dumper is provided I
        will fall back to config.
        """
        self.local = local
        self.config = config or JsonSkinConfig()
        self.parent_skin = parent
        self.dumper = dumper or self.config

    def get(self, attr, parent=True, local=True, config=True, append=True, **kw):
        """
        Resolve the value of attr. Look in local storage (programmatically
        created) then in loaded configuration (from file possibly) and
        finally pass the question to the parent skin. You may omit any
        of the above lookups with the corresponding attrubute.

        If an attribute is of type list or dict and append is True
        then I will concatenate all the values I find. Shallow tells
        me to not do any processing.
        """

        ret = None
        sources = self._available_sources(parent, local, config)

        for s in sources:
            # Assume attribute types are consistent
            val = s.get(attr)

            if val:
                if type(ret) is list and append:
                    ret += val
                elif type(ret) is dict and append:
                    ret.update(val)
                elif ret is None:   # If nothing useful was found.
                    ret = val

        return ret

    def _available_sources(self, parent=True, local=True, config=True):
        return  [ i for i in
                  (local and self.local,
                   config and self.config,
                   parent and self.parent_skin)
                  if i]

    def append(self, attr, val, coll_type=list, **kw):
        """
        Append the attribute to the value. This only affects local
        configuration. Append will assume val is supposed to be an
        empty list if unset. If i cannot decide weather `attr`
        corresponds to a dict or a list `coll_type` will tell me.

        Also note that this is more of a 'push' than an append.
        """

        # Skin subclasses may or may not process their data. Shallow
        # tells them we are not actually interested in the actual
        # values.
        cv = self.get(attr, shallow=True)

        # Make a val of the correct type
        try:
            rval = type(cv)([val])
        except TypeError:
            rval = coll_type([val])

        # Register to local
        try:
            # Assume it's a dict
            self.local[attr].update(rval)
        except KeyError:        # attr not in local
            self.local[attr] = rval
        except AttributeError:  # attr not a dict
            self.local[attr] = rval + self.local[attr]
        except TypeError:       # local does not exist
            self.local = {attr: rval}


    def set(self, attr, val, depth=0, **kw):
        """
        Set the value for the programmatic interface. Depth show how deep
        in the parent skins to set it. Use `append` to populate list
        or dict variables.
        """

        if depth == 0:
            try:
                self.local[attr] = val
            except TypeError:
                self.local = dict([(attr,val)])
            else:
                if self.parent_skin is None:
                    self.parent_skin = Skin()

        else:
            self.parent_skin.set(attr, val, dapth-1)

        return val


    def set_dumper(self, dumper):
        """
        Set the dumper.
        """

        self.dumper = dumper


    def set_parent(self, parent):
        """
        Set the dumper.
        """

        self.parent_skin = parent


    def set_config(self, config):
        """
        Set the read config provider.
        """

        self.config = config

    def keys(self, parent=True, local=True, config=True):

        return set(reduce(lambda x,y: x + list(y.keys()),
                          self._available_sources(parent, local, config),
                          []))


    def dump(self, parent=True, local=True, config=True):
        # Note that we do not use update or sth like that to keep the
        # amount of methods of configs to a minimum.
        keys = self.keys(parent, local, config)
        data = {}

        for k in set(keys):
            data[k] = Skin.get(self, k, shallow=True)

        return self.dumper.dump(data)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        return self.set(key, val)
