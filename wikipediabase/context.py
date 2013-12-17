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
        it. `function` declares wether the skin can handle functions.
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
    def register_function(cls, fn, name=None, domain="functions", skin=None):
        """
        Register a function and bind it with a name under a certain domain.
        """

        s = skin or cls.get_skin(function=True)
        s.append(domain, (name or fn.__name__, fn), coll_type=dict)

    @classmethod
    def append_function(cls, fn, domain="attributes_generators", skin=None):
        """
        Append a function object to a domain.
        """

        s = skin or cls.get_skin(function=True)
        s.append(domain, fn)

    @classmethod
    def set_function(cls, fn, domain="front_end", skin=None):
        """
        Set a single method to domain
        """

        s = skin or cls.get_skin(function=True)
        s.set(domain, fn)
