"""

"""


from functions import FunctionSkin
from skin import Skin

class Context(object):
    """
    Context is a namespace that manages the stack of skins.
    """

    _skin = None

    @classmethod
    def get_skin(cls, function=False):
        """
        See if this skin will do. If not create an overlay skin and return
        it.
        """

        if cls._skin is None or (function and not isinstance(cls._skin, FunctionSkin)):
            return cls.set_skin(function and FunctionSkin() or Skin())

        return cls._skin


    @classmethod
    def set_skin(cls, skin, child=True):
        """
        Add a layer overlay to skin. Set it as a child to the previous?
        """

        if child:
            skin.set_parent(cls._skin)

        cls._skin = skin
        return cls._skin


    @classmethod
    def register_function(cls, fn, name=None, skin=None):
        """
        Register functiion named name under a function skin.
        """

        s = skin or cls.get_skin(function=True)

        s.add_function(fn, name=name)


def wbcall(name, *args, **kwargs):
    return Context.get_skin(function=True).call(name, *args, **kwargs)

def wbregister(fn):
    """
    Register this function using its name as name.
    """

    Context.register_function(fn)
    return fn


def wbregister_named(name):
    """
    Decorator to register fuction under name.
    """

    def real_dec(fn):
        Context.register_function(fn, name)
        return fn

    return real_dec
