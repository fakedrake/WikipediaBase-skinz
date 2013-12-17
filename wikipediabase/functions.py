import importlib
import types

from wikipediabase.skin import Skin

class SerialFunction(object):
    """
    This is a serializable/deserializable function.
    """

    def __init__(self, serial=None, fn=None):
        """
        Create a serialfunc from a tuple or a string.
        """

        if not hasattr(fn, '__call__'):
            raise TypeError("SerialFunction can be created only for callables.")

        self.tup = serial
        self.fn = fn


    def _fn_class(self):
        try:
            return self.fn.im_class.__name__
        except AttributeError:
            return None

    def serial(self):
        """
        Return a tuple that one can turn into this function
        """

        if self.fn:
            self.tup = self.fn.__module__, self._fn_class(), self.fn.__name__

        return self.tup

    def deserial(self):
        if self.tup:
            mn, cn, fn = self.tup
            m = importlib.import_module(mn)
            c = cn and getattr(m, cn) or m
            self.fn = getattr(c, fn)

        return self.fn

    def __str__(self):
        return str(self.serial())

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

    def get(self, name):
        """
        Call function given by name wnith arguments.
        """

        val = super(FunctionSkin, self).get(name)

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

        try:
            return fun.deserial()
        except AttributeError:
            return fun

    def _fn_serial(self, fn):
        """
        Maybe serialize function. If not function just return the value.
        """

        if isinstance(fn, SerialFunction):
            return fn

        try:
            return SerialFunction(fn=fn)
        except TypeError:
            return fn

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
