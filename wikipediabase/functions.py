import importlib
import types

from wikipediabase.skin import Skin


def _serial(fn):
    """
    Return a tuple that one can turn into this function
    """

    return (fn.__module__, _fn_objpath(fn), fn.__name__)

def _fn_objpath(fn):

    if hasattr(fn, 'ad_objpath'):
        return fn.ad_objpath

    return []

class MetaAdvert(type):
    """
    Add an ad_class attribute to functions so the Skin can find them.
    """

    def __new__(meta, clsname, bases, clsDict):
        """
        Add the class name to the registered functions so that they are
        locatable and also turn registered methods into static
        methods.
        """

        statix = {}

        for k, v in clsDict.iteritems():
            if hasattr(v, '__func__'):
                v = v.__func__
            elif type(v) is types.FunctionType and hasattr(v, 'ad_entry'):
                statix[k] = staticmethod(v)

            if hasattr(v, "__call__"):
                setattr(v, 'ad_objpath', [clsname])

            # If a serial function was created for this fix it.
            if hasattr(v, 'ad_entry'):
                m, obp, n = v.ad_entry
                obp.append(clsname)

        clsDict.update(statix)
        return type.__new__(meta, clsname, bases, clsDict)


class SerialFunction(tuple):
    """
    This is a serializable/deserializable function. It is also a list
    so it can be serialized.
    """

    def __new__(cls, serial=None, fn=None):
        """
        Create a serialfunc from a tuple or a string.
        """

        if not hasattr(fn, '__call__'):
            raise TypeError("SerialFunction can be created only for callables.")

        return super(SerialFunction, cls).__new__(cls, tuple(serial or _serial(fn)))

    def __init__(self, serial=None, fn=None):

        if fn and type(fn) is types.FunctionType:
            setattr(fn, 'ad_entry', self)

    def deserial(self):
        if not hasattr(self, "fn"):
            mn, op, fn = self
            m = importlib.import_module(mn)
            c = reduce(lambda m,on: getattr(m, on), op, m) # Walk the object path
            self.fn = getattr(c, fn)

        return self.fn

    def __repr__(self):
        return "<SerialFunction object of '%s'>" % repr(self.deserial())


class FunctionSkin(Skin):
    """
    A skin that is aware of functions and stores them along with their
    module so that they can be retireieved. Dont overuse this as it is
    not 100% clear when we have a 'serialized' function and when a
    random tuple.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize yourself using a dict-like list of funtions and an
        attrname.
        """

        super(FunctionSkin, self).__init__(*args, **kwargs)

    def get(self, name, shallow=False, **kw):
        """
        Call function given by name wnith arguments. Shallow means dont do
        any processing on the data before returning it.
        """

        val = super(FunctionSkin, self).get(name, shallow=shallow, **kw)

        if shallow:
            return val

        if type(val) is dict:
            return dict([(n,self._fn_deserial(f)) for n, f in val.items()])
        elif type(val) is list:
            return [self._fn_deserial(f) for f in val]
        else:
            return self._fn_deserial(val)

    def _fn_deserial(self, fun):
        """
        Assume this is a serialized function and return it. If it does not
        even match the
        """

        if isinstance(fun, SerialFunction):
            return fun.deserial()
        elif hasattr(fun, '__iter__') and len(fun) == 3: # It is a tuple
            return SerialFunction(serail=fun).deserial()

        return fun

    def _fn_serial(self, fn):
        """
        Maybe serialize function. If not function just return the value.
        """

        if isinstance(fn, SerialFunction):
            return fn

        return SerialFunction(fn=fn)

    def set(self, attr, val, depth=0):
        """
        If we encounter a function save it in a meaningful way.
        """

        val = self._fn_serial(val)

        return super(FunctionSkin, self).set(attr, val)

    def append(self, attr, val, coll_type=list):
        key = None
        try:
            key, fn = val
            fn = self._fn_serial(fn)
            val = (key,fn)
        except TypeError:
            fn = self._fn_serial(val)

        return super(FunctionSkin, self).append(attr, val, coll_type)
