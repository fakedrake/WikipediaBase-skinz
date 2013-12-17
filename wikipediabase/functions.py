import importlib
import types

from wikipediabase.skin import Skin

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

        val = super(FunctionSkin, self).set(name)

        if type(val) is dict:
            return dict([(n,self._fn_seserial(f)) for n, f in val.items()])
        elif type(val) is list:
            return [self._fn_seserial(f) for f in val]
        else:
            return _fn_deserial(val)

    def _fn_deserial(self, fun):
        try:
            mn, fn = fun
        except TypeError:
            return fun

        m = importlib.import_module(mn)
        return getattr(m, fn)

    def _fn_serial(self, fn):
        """
        Maybe serialize function. If not function just return the value.
        """

        if type(val) is types.FunctionType:
            return (fn.__module__, fn.__name__)

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

        return super(FunctionSkin, self).append(attr, val, dict_like)
