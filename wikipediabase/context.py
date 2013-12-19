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
        it. If you want a specific skin type use 'set_skin' and then this.

        - function: Specify that you will need the skin for storing
          functions. Will overlay a new one.
        """

        iscorrect = function and isinstance(cls._skin, FunctionSkin) or \
                    cls._skin is None

        if iscorrect:
            cls.set_skin(function and FunctionSkin() or Skin())

        return cls._skin


    @classmethod
    def set_skin(cls, skin, child=True):
        """
        Add a layer overlay to skin.

        - skin: skin to replace with
        - child: False ignores all the so-far structure and replaces.
        """

        if child:
            skin.set_parent(cls._skin)

        cls._skin = skin
        return cls._skin


    @classmethod
    def register_function(cls, fn, name=None, domain=None, skin=None, append=True, mapping=True, **kw):
        """
        Register a function under domain.

        - name: Give a name to the function. Fallback to function name
        - domain: Skin domain. Fallback to name
        - skin: Use specific skin (not appended)
        - append: the domain is a collection. Append to it.
        - mapping: the domain is a mapping, ignore if not appending
        """

        s = skin or cls.get_skin(function=True)
        name = name or fn.__name__
        domain = domain or name

        # XXX: this might not be the place to interpret append == None
        # as append == True
        if append or append is None:
            if mapping:
                s.append(domain, (name, fn), coll_type=dict)
            else:
                s.append(domain, fn, coll_type=list)
        else:
            s.set(domain or name, fn)
